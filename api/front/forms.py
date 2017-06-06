# coding:utf8

from django import forms
from api.common.forms import BaseForm
from django.core.cache import cache

class CaptchaForm(forms.Form):
    captcha = forms.CharField(max_length=4,min_length=4)
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        if not cache.get(captcha):
            raise forms.ValidationError(u'验证码错误')
        return captcha

class FrontRegistForm(BaseForm,CaptchaForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=20,min_length=2)
    password = forms.CharField(max_length=20,min_length=6)

class FrontLoginForm(BaseForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.BooleanField(required=False)

class FrontEmailForm(BaseForm):
    email = forms.EmailField()

class FrontResetPwd(BaseForm):
    password = forms.CharField(max_length=20,min_length=6)
    password_repeat = forms.CharField(max_length=20,min_length=6)

    def clean(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError(u'两次密码不一致')
        else:
            return self.cleaned_data

class AddCommentForm(BaseForm):
    article_id = forms.CharField(max_length=128)
    content = forms.CharField()