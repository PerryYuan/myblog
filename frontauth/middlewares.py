# coding:utf8

from django.utils.deprecation import MiddlewareMixin
from models import FrontUserModel
import configs
class FrontAuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        uid = request.session.get(configs.FRONT_SESSION)
        if uid:
            user = FrontUserModel.objects.filter(uid=uid).first()
            if not hasattr(request,'front_user'):
                setattr(request,'front_user',user)