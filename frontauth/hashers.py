# coding:utf8

import hashlib
import configs

def make_password(password,salt=None):
    if not salt:
        salt = configs.FRONT_SALT
    return hashlib.md5(salt+password).hexdigest()

def check_password(raw_password,password,salt=None):
    return raw_password and password == make_password(raw_password,salt)
