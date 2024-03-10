# api-auth


## Usage

~~~
http POST http://localhost:8000/auth/users/ email=me@example.com password=secret

http -f POST http://localhost:8000/auth/token username=me@example.com password=secret
~~~

## Developer cheatsheet
### Alembic cheatsheet
~~~
alembic revision --autogenerate -m "some desc"
alembic upgrade head
alembic current
~~~