# coding:utf8
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from mutils.captcha.xtcaptcha import Captcha

try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
def captcha(request):
    text,image = Captcha.gene_code()
    out = StringIO()
    image.save(out,'png')
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    return response
