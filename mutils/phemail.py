# coding:utf8
import hashlib
import time
from django.core.cache import cache
from django.shortcuts import redirect,reverse
from django.core import mail
from django.conf import settings

def send_email(request,email,check_url,check_data=None,subject=None,message=None):
    code = hashlib.md5(str(time.time()) + email).hexdigest()
    if check_data:
        cache.set(code, check_data, 120)
    else:
        cache.set(code, email, 120)
    url = request.scheme + '://' + request.get_host() + reverse(check_url, kwargs={'code': code})
    if not subject:
        subject = u'修改邮箱'
    if not message:
        message = u'请点击以下链接确认修改邮箱 ' + url
    else:
        message += url
    if mail.send_mail(subject, message, settings.EMAIL_HOST_USER, [email]):
        return True
    return False