from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
import uuid
from .settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_uuid(db: Session, uuid: str):
    return db.query(models.User).filter(models.User.uuid == uuid).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_login(db: Session, login: str):
    if settings.username_is_email:
        return get_user_by_email(db=db, email=login)
    else:
        return get_user_by_username(db=db, username=login)


def get_auth_user(db: Session, login: str, password: str):
    user = get_user_by_login(db, login)
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    if settings.username_is_email:
        username = user.email
    else:
        username = user.username

    db_user = models.User(email=user.email, username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


