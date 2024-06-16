class SimpleAuthException(Exception):
    pass

class SimpleAuthVerificationAlreadySent(SimpleAuthException):
    pass

class SimpleAuthCaptchaFailed(SimpleAuthException):
    pass