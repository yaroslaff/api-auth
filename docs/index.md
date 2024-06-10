# FastAPI-Simple-Atuh

## Simple authentication for FastAPI

Install in two commands, add authentication in three lines, configure to taste.

[FastAPI-Simple-Auth git repository](https://github.com/yaroslaff/fastapi-simple-auth)
[FastAPI-Simple-Auth documentation](https://fastapi-simple-auth.readthedocs.io/)

## Features
- Users are stored in any supported SQLAlchemy database (sqlite3, mysql, ...)
- Optional email verification
- User creation
- Password recovery
- Profile page with change password, change email
- Custom UI themes!


## Example protected app
~~~python
from fastapi import FastAPI
from fastapi_simple_auth import SimpleAuth, logged_in_user
        
app = FastAPI()

simpleauth = SimpleAuth(app)

@app.get("/")
async def read_users_me(user: logged_in_user) -> str:    
    return f"Hello {user.username} {user.uuid}"
~~~

## Install

> **Note**: use virtualenv.

~~~shell
pip3 install fastapi-simple-auth
# create/edit .env file
vim .env
simpleauth dbupgrade
~~~

Write app in app.py

Start:
~~~
uvicorn app:app
~~~

## Official Documentation location
https://fastapi-simple-auth.readthedocs.io/

Source for documentation are in 
