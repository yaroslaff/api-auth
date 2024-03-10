from .settings import settings
from .verification import generate_code
from .session import session_startup
from fastapi import FastAPI


def startup(app: FastAPI):
    """ initialize auth and test settings """
    print(settings)

    code = generate_code()
    print("TEST generate code:", code)

    assert(settings.auth_transport in ['session', 'jwt'])

    if settings.auth_transport == "session":
        # session_startup(app)
        pass