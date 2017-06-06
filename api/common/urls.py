# coding:utf8
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^captcha$', views.captcha, name='comm_captcha'),
]