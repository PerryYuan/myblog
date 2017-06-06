from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CMSUser(models.Model):
    avatar = models.URLField(max_length=100,blank=True)
    user = models.OneToOneField(User)
