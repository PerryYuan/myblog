#coding:utf8

from django.db import models
from uuid import uuid4
import hashers
# Create your models here.

class FrontUserModel(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid4)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    _password = models.CharField(max_length=128)
    avatar = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    join_time = models.DateTimeField(auto_now_add=True)

    def __init__(self,*args,**kwargs):
        super(FrontUserModel,self).__init__(*args,**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = hashers.make_password(raw_password)
        self.save()

    def check_password(self,raw_password):
        return hashers.check_password(raw_password,self.password)


