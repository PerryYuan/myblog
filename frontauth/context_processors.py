# coding:utf8
import configs
from models import FrontUserModel

def auth(request):
    uid = request.session.get(configs.FRONT_SESSION)
    if uid:
        if hasattr(request,'front_user'):
            return {'front_user':request.front_user}
        else:
            user = FrontUserModel.objects.filter(uid=uid).first()
            if user:
                return {'front_user':user}
    return {}