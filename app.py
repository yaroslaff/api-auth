
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware

from fastapi_simple_auth import auth_router, logged_in_user
from fastapi_simple_auth.views import User


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='ChangeMe', max_age=None)

app.include_router(auth_router, prefix="/auth")

app.mount("/static", StaticFiles(packages=['fastapi_simple_auth']), name="static")

# app.mount('/auth', api_auth)

@app.get("/users/me/", response_model=User)
async def read_users_me(
    user: logged_in_user
):
    print("VIEW USER:", user)
    print(type(user))
    print(dir(user))
    return user

@app.get("/users/me/items/")
async def read_own_items(
    user: logged_in_user
):
    return [{"item_id": "Foo", "owner": user.username}]