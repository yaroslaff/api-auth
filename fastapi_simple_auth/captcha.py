import requests

from fastapi import Request
from .settings import settings
from .exceptions import SimpleAuthCaptchaFailed

def verify_turnstile_captcha(remote_ip: str, token: str):

    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    form = {
        'secret': settings.turnstile_secret,
        'response': token,
        'remote_ip': remote_ip
    }    	
        
    r = requests.post(url, data=form)
    rj = r.json()
    if r.status_code == 200 and rj['success'] == True:
        return 
    
    if r.json()['success'] == False:
        print("CAPTCHA VERIFICATION:", rj)
        if 'missing-input-response' in rj['error-codes']:
            raise SimpleAuthCaptchaFailed("Empty captcha")
    
        if 'invalid-input-response' in rj['error-codes']:
            raise SimpleAuthCaptchaFailed("Invalid captcha token")

    raise SimpleAuthCaptchaFailed("captcha error")
    

def verify_captcha(rq: Request, token: str ):

    remote_ip = rq.client.host
    
    if settings.turnstile_sitekey and settings.turnstile_secret:
        return verify_turnstile_captcha(remote_ip=remote_ip, token=token)
