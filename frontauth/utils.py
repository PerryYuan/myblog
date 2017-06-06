# coding:utf8
from models import FrontUserModel
import configs

def login(request,email,password):
    user = FrontUserModel.objects.filter(email=email).first()
    if user:
        if user.check_password(password):
            request.session[configs.FRONT_SESSION] = str(user.pk)
            return user
        return None
    return None

def logout(request):
    try:
        del request.session[configs.FRONT_SESSION]
    except KeyError:
        pass