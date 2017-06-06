from __future__ import unicode_literals

from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from frontauth.models import FrontUserModel
# Create your models here.

class ArticleModel(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid4)
    author = models.ForeignKey(User,null=False)
    title = models.CharField(max_length=20)
    desc = models.CharField(max_length=100,blank=True)
    thumbnail = models.URLField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey('CategoryModel')
    tags = models.ManyToManyField('TagModel',blank=True)

    create_time = models.DateTimeField(auto_now_add=True,null=True)
    update_time = models.DateTimeField(auto_now=True,null=True)
    read_count = models.IntegerField(default=0)

    top = models.ForeignKey('TopModel',null=True,on_delete=models.SET_NULL)

class CategoryModel(models.Model):
    name = models.CharField(max_length=20,unique=True)

class TagModel(models.Model):
    name = models.CharField(max_length=20,unique=True)

class TopModel(models.Model):
    create_time = models.DateTimeField(auto_now=True)


class CommentModel(models.Model):
    author = models.ForeignKey(FrontUserModel)
    content = models.TextField()
    article = models.ForeignKey('ArticleModel')
    create_time = models.DateTimeField(auto_now_add=True)
