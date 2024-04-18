from fastapi import Request
from fastapi.responses import HTMLResponse

from ..router import auth_router
from ..templates import template_env
from ..settings import settings
from ..pub import logged_in_user

@auth_router.get('/profile')
def profile_get(request: Request, user: logged_in_user, response_class=HTMLResponse):
    tpl = template_env.get_template('profile.html')

    ctx = {
        'rq': request,
        'settings': settings,
        'user': user,
    }

    html = tpl.render(ctx)
    return HTMLResponse(html)
