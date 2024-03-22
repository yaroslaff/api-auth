from .settings import settings
from .templates import template_env
from .models import User, Code
from .envmail import send_mail

from fastapi import Request

import string
import random
import datetime

from sqlalchemy.orm import Session

codesets = {
    "digits": string.digits,
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "letters": string.ascii_letters
}

def generate_code():
    try:
        codeset = codesets[settings.code_set]
    except KeyError as e:
        raise KeyError(f'CODE_SET must be one of: { " ".join(codesets) }')

    code = ''.join(random.choice(codeset) for i in range(settings.code_size))
    return code


def send_verification(request: Request, db: Session, user: User):
    code_value = generate_code()
    print("verification code:", code_value)

    expires = datetime.datetime.now() + datetime.timedelta(seconds=settings.code_lifetime)
    print("exp:", expires)

    code_record = Code(code=code_value, purpose="verification", expires=expires)
    db.add(code_record)
    db.commit()


    tpl = template_env.get_template('confirm-email.html')

    html = tpl.render(code = code_value, title = settings.app_title, email = user.email)
    
    print("HTML:", html)
    send_mail(user.email, subject=f"Registration on {settings.app_title}", html=html)
    