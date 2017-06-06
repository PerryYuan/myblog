# coding:utf8
from functools import wraps
import configs
from django.shortcuts import reverse,redirect

def front_login_require(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        uid = request.session.get(configs.FRONT_SESSION)
        if uid:
            return func(request,*args,**kwargs)
        else:
            url = reverse('front_login')+'?next='+ request.path
            return redirect(url)

    return wrapper