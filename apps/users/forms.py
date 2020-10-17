# -*- coding = utf-8 -*-
# @Time :
# @ Author : Yeeero
# @File : forms.by
# @Software : PyCharm

from django import forms
import captcha
from captcha.fields import CaptchaField
from users.models import *


class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=15, error_messages={
        'required': '密码不能为空',
        'min_length': '密码不能少于3位',
        'max_length': '密码不能超过15位',
    })
    captcha = CaptchaField()


# 用户登录验证
class UserLoginForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3, max_length=15, error_messages={
        'required': '密码不能为空',
        'min_length': '密码不能少于3位',
        'max_length': '密码不能超过15位',
    })


class UserForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


class UserResetForm(forms.Form):
    password = forms.CharField(required=True, min_length=3, max_length=15, error_messages={
        'required': '密码不能为空',
        'min_length': '密码不能少于3位',
        'max_length': '密码不能超过15位',
    })
    password2 = forms.CharField(required=True, min_length=3, max_length=15, error_messages={
        'required': '密码不能为空',
        'min_length': '密码不能少于3位',
        'max_length': '密码不能超过15位',
    })


class UserChangeImageForm(forms.ModelForm):  # 上传图片验证
    class Meta:
        model = UserProfile
        fields = ['image']


class UserChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'phone']


class UserChangeEmailForm(forms.ModelForm):     # 修改邮箱验证
    class Meta:
        model = UserProfile
        fields = ['email']