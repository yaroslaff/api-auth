# api-auth

## Authentication easy as three lines!

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

## Features
- Users are stored in any supported SQLAlchemy database
- Optional email verification
- User creation
- Password recovery
- Custom UI themes!


## Install

~~~shell
cp .env.example .env
# now edit it
vim .env

alembic upgrade head
~~~


## Usage

~~~
# register
http POST http://localhost:8000/auth/users/ username=me@example.com password=secret

# simple auth (session)
http -f POST http://localhost:8000/auth/login username=me@example.com password=secret

# get token
http -f POST http://localhost:8000/auth/token username=me@example.com password=secret
~~~

## Developer cheatsheet
### Alembic cheatsheet
~~~
alembic revision --autogenerate -m "some desc"
alembic upgrade head
alembic current
~~~