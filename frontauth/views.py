#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from models import FrontUserModel
from utils import login,logout
from decorators import front_login_require
# Create your views here.

def add_front_user(request):
    email = 'xxx1.@qq.com'
    password = '11132'
    # username = 'bbb'
    # user = FrontUserModel(email=email,username=username,password=password)
    # user.save()
    user = FrontUserModel.objects.filter(email=email).first()
    print user.password
    user.password = password
    print user.password
    return HttpResponse('ok')

def test(request):
    email = 'xxx1.@qq.com'
    password = '11132'
    if login(request,email,password):
        return HttpResponse('ok')
    return HttpResponse('fail')

def test1(request):
    logout(request)
    return HttpResponse('ok')

@front_login_require
def test2(request):
    print request.front_user
    return HttpResponse('ok')



