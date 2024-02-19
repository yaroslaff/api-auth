
from fastapi import Depends, FastAPI
from dotenv import load_dotenv

from auth import api_auth, logged_in_user, User

app = FastAPI()
app.include_router(api_auth, prefix="/auth")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    user: logged_in_user
):
    return user


@app.get("/users/me/items/")
async def read_own_items(
    user: logged_in_user
):
    return [{"item_id": "Foo", "owner": user.username}]