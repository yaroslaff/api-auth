from datetime import datetime, timedelta, timezone
from typing import Annotated
import logging

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from jose import JWTError, jwt
from pydantic import BaseModel

from fastapi import APIRouter

from sqlalchemy.orm import Session

from . import schemas, crud
from .db import get_db
from .settings import settings
from .verification import send_verification
from .templates import template_env
from .startup import startup
from .session import get_current_user_session

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# suppress AttributeError: module 'bcrypt' has no attribute '__about__'
logging.getLogger('passlib').setLevel(logging.ERROR)

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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

api_auth = APIRouter()
# api_auth = FastAPI()

startup(api_auth)

# api_auth.mount("/static", StaticFiles(directory="static"), name="static")


#def get_user(db, username: str):
#    if username in db:
#        user_dict = db[username]
#        return UserInDB(**user_dict)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




async def get_current_user_jwt(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(request: Request, db: Session = Depends(get_db)):
    if settings.auth_transport == "session":
        print("call get current user session")
        return get_current_user_session(request, db)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    print("curuser:", current_user)
    #if current_user.disabled:
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


logged_in_user = Annotated[User, Depends(get_current_active_user)]

@api_auth.get('/login')
def login_html():
    tpl = template_env.get_template('login.html')

    ctx = {
        'motd2': 'motd motd motd motd motd motd',
        'error2': 'some problem'
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)


@api_auth.post('/login')
def login_html(
            request: Request, 
            form: Annotated[OAuth2PasswordRequestForm, Depends()],
            db: Session = Depends(get_db),
            response_class=HTMLResponse):
    
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
        request.session['user'] = user.uuid        



@api_auth.post("/token")
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


@api_auth.post("/users/", response_model=schemas.User)
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    if settings.username_is_email:
        db_user = crud.get_user_by_email(db, email=user.email)
    else:
        db_user = crud.get_user_by_username(db, username=user.username)

    
    print("pre-registered user:", db_user)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    user = crud.create_user(db=db, user=user)
    print("created user", user)

    if settings.email_verification:
        send_verification(request=request, db=db, user=user)
    
    return user