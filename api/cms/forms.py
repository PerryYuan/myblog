# coding:utf8
from django import forms
from mutils.captcha.xtcaptcha import Captcha
from api.common.forms import BaseForm



class LoginForm(BaseForm):
    username = forms.CharField(max_length=10,min_length=2,error_messages={'min_length':u'用户名格式不正确','max_length':u'用户名格式不正确'})
    password = forms.CharField(max_length=20,min_length=6,error_messages={'min_length':u'密码格式不正确','max_length':u'密码格式不正确'})
    captcha = forms.CharField(max_length=4,min_length=4,error_messages={'min_length':u'验证码格式不正确','max_length':u'验证码格式不正确'})
    remember = forms.BooleanField(required=False)
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha',None)
        if  not Captcha.check_captcha(captcha):
            raise forms.ValidationError(u'验证码错误')
        return captcha

class UpdateProfileForm(BaseForm):
    username = forms.CharField(max_length=10, min_length=2,error_messages={'min_length': u'用户名格式不正确', 'max_length': u'用户名格式不正确'})
    avatar = forms.URLField(required=False)

class UpdateEmailForm(BaseForm):
    email = forms.EmailField(required=True,error_messages={'required':u'必须写入邮箱'})

class AddCategoryForm(BaseForm):
    name = forms.CharField(max_length=20)

class AddTagForm(BaseForm):
    name = forms.CharField(max_length=20)

class AddArticleForm(BaseForm):
    title = forms.CharField(max_length=20)
    category = forms.IntegerField()
    desc = forms.CharField(max_length=100,required=False)
    thumbnail = forms.URLField(max_length=100)
    content = forms.CharField()

class UpdateArticleForm(AddArticleForm):
    uid = forms.UUIDField()

class DeleteArticleForm(BaseForm):
    uid = forms.UUIDField()

class TopArticleForm(DeleteArticleForm):
    pass

class CategoryForm(BaseForm):
    id = forms.IntegerField()

class CategoryEditerForm(CategoryForm):
    name = forms.CharField()

