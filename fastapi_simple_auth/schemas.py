from pydantic import BaseModel, EmailStr, create_model
from typing import Optional
from .settings import settings

if settings.username_is_email:
    username_type = EmailStr
else:
    username_type = str

class UserBase(BaseModel):
    username: username_type

# create UserBase dynamically because email XOR username
if False:
    if settings.username_is_email:

        # Simplest. Username (batman@example.com) is email (no special username)

        UserBase = create_model(
            'UserBase', username=(str, None)
        )
    else:
        if settings.email_verification:
            # user: email required (user: batman2000 email: batman@example.com)
            UserBase = create_model(
                'UserBase', username=(str, None), email=(EmailStr)
            )
        else:
            # no verification, (user: batman2000)
            UserBase = create_model(
                'UserBase', username=(str, None), email=(Optional[EmailStr], None)
            )


class UserCreate(UserBase):
    password: str

class User(UserBase):
    uuid: str
    is_active: bool

    class Config:
        from_attributes=True
