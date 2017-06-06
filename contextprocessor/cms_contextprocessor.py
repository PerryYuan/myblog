# coding:utf8
from cmsauth.models import CMSUser

def CmsContextProcessor(request):
    user = request.user
    if not hasattr(user,'avatar'):
        cms_user = CMSUser.objects.filter(user__pk=user.pk).first()
        if cms_user:
            setattr(user,'avatar',cms_user.avatar)
    return {'user':user}