
import json
from typing import Annotated
from pydantic import BaseModel, EmailStr

from fastapi import Request, Response, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from ..router import auth_router
from ..templates import template_env
from ..settings import settings

from .. import crud, schemas
from ..db import get_db
from ..verification import send_verification, get_code_record
from ..exceptions import SimpleAuthVerificationAlreadySent
from ..cron import cron

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


#class UNUSED_UserInDB(User):
#    hashed_password: str


@auth_router.get('/settings.js')
def settings_view(request: Request):
    
    data = {
        'username_is_email': settings.username_is_email,
        'signin_after_signup': settings.signin_after_signup,
        'afterlogin_url': settings.afterlogin_url,
        'afterlogout_url': settings.afterlogout_url
    }
    
    js_content = f"""
    const settings = {json.dumps(data)};
    sessionStorage.setItem("simpleAuthSettings", JSON.stringify(settings));
    """

    response = Response(content=js_content, media_type="application/javascript")

    return response

@auth_router.get('/register')
def register_html(request: Request, response_class=HTMLResponse):
    tpl = template_env.get_template('register.html')

    ctx = {
        'rq': request,
        'settings': settings,
        'motd2': 'motd motd motd motd motd motd',
        'error2': 'some problem'
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)

@auth_router.get('/emailverify/{email}')
def email_verify_get(rq: Request, email: str, db: Session = Depends(get_db)):

    # get code record
    user = crud.get_user_by_username(db=db, username=email)
    cr = get_code_record(db=db, user=user, purpose='signup')
    msg = None
    if cr:
        msg = f'Message to {user.username} was sent at {cr.created}'
        

    tpl = template_env.get_template('verify-email.html')
    ctx = {
        "rq": rq,
        "settings": settings,
        "email": email,
        "message": msg
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)

@auth_router.post('/emailverify/{email}')
def email_verify_post(rq: Request, email: str, coderq: schemas.VerificationCode, db: Session = Depends(get_db)):
    
    resp_bad = Response(status_code=400, content="Bad code")
    code = coderq.code
    user = crud.get_user_by_username(db=db, username=email)
    cr = get_code_record(db=db, user=user, purpose='signup')
    success = {
            'text': 'Verification successful! You can login now!',
            'url': str(rq.url_for('login_get'))
        }
    
    if not cr:
        return resp_bad
    
    cron(db)

    if cr.code == code:
        user.email_verified = True
        cr.delete()
        db.commit()
        return success
    else:
        return resp_bad



@auth_router.get('/login')
def login_get(request: Request, response_class=HTMLResponse):
    tpl = template_env.get_template('login.html')

    ctx = {
        'rq': request,
        'settings': settings,
        'motd2': 'motd motd motd motd motd motd',
        'error2': 'some problem'
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)

@auth_router.post('/login')
def login_post(
            rq: Request, 
            form: Annotated[OAuth2PasswordRequestForm, Depends()],
            db: Session = Depends(get_db)):

    # here is POST
    user = crud.get_auth_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


    # authenticate
    if settings.auth_transport == "session":
        rq.session['user'] = user.uuid        

    return {
        'status': 'OK',
        'url': settings.afterlogin_url
    }

@auth_router.post('/logout')
def logout(rq: Request):
    if settings.auth_transport == "session":
        del rq.session['user']
    return RedirectResponse(settings.afterlogout_url)


@auth_router.post("/token")
async def login_for_access_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    
    user = crud.get_auth_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.uuid}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@auth_router.post("/users/") # , response_model=schemas.User)
def create_user(rq: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = crud.get_user_by_username(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    user = crud.create_user(db=db, user=user)
    if settings.username_is_email:
        try:
            send_verification(rq, db=db, user=user)
            return {"status": "OK", 
                    "message": "Please check your email for verification code",
                    "redirect": str(rq.url_for("email_verify_get", email=user.username))
                    }
        
        except SimpleAuthVerificationAlreadySent as e:
            print("ERR", e)
    else:
        print("created user", user)    
        if settings.signin_after_signup:
            # authenticate user
            if settings.auth_transport == "session":
                rq.session['user'] = user.uuid        
                return {"status": "OK", 
                        "redirect": settings.afterlogin_url }
        else:
            return {"status": "OK", 
                    "message": "Please check your email for verification code",
                    "redirect": settings.afterlogin_url }

    
    print("return")
    # return user
    return Response()
