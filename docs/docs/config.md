# Configuration settings

Configuration settings are defined in settings.py and should be configured either using environment variables
or using .env file

## Application
### APP_TITLE
title of application, default: "My Noname App"

### SECRET_KEY
random secret key. generate it with python:
~~~
"".join(random.choices(string.ascii_letters + string.digits, k=50))
~~~

or from this shell one-lines:
~~~
< /dev/urandom tr -dc '[:alnum:]_$#%-' | head -c50; echo
~~~


## Database
### DB_URL
Address of database, default: `sqlite:///./test.db`

## Authentication

### AUTH_TRANSPORT
default: "session"

Where we hold successful authentication

### USERNAME_IS_EMAIL
If Yes, all usernames must be email addresses (e.g. batman2000@hotmail.com) and will be verified.
If no, usernames are just strings (e.g. batman2000) and not verified



## Code generation
Recovery and verification codes are generated based on these settings:
~~~
    code_size: int = 6
    code_set: str = "digits"
    code_lifetime: int = 86400
    code_regenerate: int = 30
~~~


## Sending mail
~~~
    mail_transport: str = "stdout"
    mail_host: str = "127.0.0.1"
    mail_port: int = 25
    mail_from: str = "NoReply <noreply@example.com>"
    mail_user: str | None = None
    mail_password: str | None = None
    mail_starttls: bool = False
~~~

## Cron
~~~
    cron_interval: int = 300
~~~

## Navigation
~~~
    afterlogin_url: str = "/"
    afterlogout_url: str = "login"
    
    # redirect to login if not authenticated
    notauth_login: bool = True

    # authenticate automatically after signup
    signin_after_signup: bool = True
~~~

## Themes
### TEMPLATE_THEME 
Name of template theme package. Default: fastapi_simple_auth_basic
