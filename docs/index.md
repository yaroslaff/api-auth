# FastAPI-Simple-Auth

## Simple authentication for FastAPI

Install in two commands, add authentication in three lines, configure to taste.

## Links
- [FastAPI-Simple-Auth git repository](https://github.com/yaroslaff/fastapi-simple-auth)
- [FastAPI-Simple-Auth documentation](https://fastapi-simple-auth.readthedocs.io/)
- [Basic theme for FastAPI-Simple-Auth](https://github.com/yaroslaff/fastapi-simple-auth-basic)
- [Dark theme for FastAPI-Simple-Auth](https://github.com/yaroslaff/fastapi-simple-auth-dark)

## Features
- Users are stored in any supported SQLAlchemy database (sqlite3, mysql, ...)
- Optional email verification
- User creation
- Password recovery
- Flexible password strength requirements
- Profile page with change password, change email
- Easy to configure via environment / .env
- Custom UI themes!

## Installation
~~~
pip3 install fastapi-simple-auth
~~~

Optionally, configure `.env` file. Lets set just one very simple config option:
~~~
APP_TITLE="My app!"
~~~

Initialize database (sqlite3 by default) with command: `simpleauth dbupgrade`

## Example protected app

You should add just three lines to basic "hello world" type of fastapi app.

1. Import package
2. hook to app with `SimpleAuth(app)`
3. add `user: logged_in_user` to protected view

~~~python
from fastapi import FastAPI
from fastapi_simple_auth import SimpleAuth, logged_in_user
        
app = FastAPI()

simpleauth = SimpleAuth(app)

@app.get("/")
async def read_users_me(user: logged_in_user) -> str:    
    return f"Hello {user.username} {user.uuid}"
~~~

Now run it.
~~~
uvicorn app:app
~~~

Open https://localhost:8000/ you will see 
![login screenshot](img/login.png)

Next, you may [configure authentication settings for your application](config).
