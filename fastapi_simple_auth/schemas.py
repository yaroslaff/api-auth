from pydantic import BaseModel, EmailStr, create_model
from typing import Optional
from .settings import settings

if settings.username_is_email:
    username_type = EmailStr
else:
    username_type = str

class UserBase(BaseModel):
    username: username_type

class UserCreate(UserBase):
    password: str
    captcha_token: Optional[str] = None

class UNUSED_User(UserBase):
    uuid: str
    is_active: bool

    class Config:
        from_attributes=True

class CaptchaOnlyRq(BaseModel):
    captcha_token: str

class VerificationCode(BaseModel):
    code: str
    captcha_token: Optional[str] = None
    
