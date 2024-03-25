
from typing import Annotated
from pydantic import BaseModel

from fastapi import Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .router import auth_router
from .templates import template_env
from .settings import settings

from . import crud, schemas
from .db import get_db
from .verification import send_verification

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


class UserInDB(User):
    hashed_password: str


@auth_router.get('/settings')
def settings_view(request: Request):
    s = {
        'username_is_email': settings.username_is_email
    }
    return s

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


@auth_router.get('/login')
def login_html(request: Request, response_class=HTMLResponse):
    tpl = template_env.get_template('login.html')

    ctx = {
        'rq': request,
        'settings': settings,
        'motd2': 'motd motd motd motd motd motd',
        'error2': 'some problem'
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)


@auth_router.post('/logout')
def logout(request: Request):
    return RedirectResponse(settings.afterlogout_url)





@auth_router.post('/login')
def login_html(
            rq: Request, 
            form: Annotated[OAuth2PasswordRequestForm, Depends()],
            db: Session = Depends(get_db),
            response_class=HTMLResponse):

    tpl = template_env.get_template('afterlogin.html')

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

    print("login, redirect to:", settings.afterlogin_url)


    ctx = {
        'rq': rq,
        'settings': settings,
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)



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


@auth_router.post("/users/", response_model=schemas.User)
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #if settings.username_is_email:
    #    db_user = crud.get_user_by_email(db, user=user.username)
    #else:
    
    db_user = crud.get_user_by_username(db, username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    user = crud.create_user(db=db, user=user)
    print("created user", user)

    if settings.email_verification:
        send_verification(request=request, db=db, user=user)
    
    return user
    # return {"user": user, "redirect": auth_router.url_path_for('login_html')}