# -*- coding = utf-8 -*-
# @Time :
# @ Author : Yeeero
# @File : forms.by
# @Software : PyCharm
import re

from django import forms

from operations.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'phone', 'course']    # 用到的字段
        # exclude = ['add_time']
        # fields = '__all__'      # 如果用到所有的字段

    def clean_phone(self):  # 二次验证
        phone = self.cleaned_data['phone']
        com = re.compile('^0?(13[0-9]|15[012356789]|17[013678]|18[0-9]|14[57])[0-9]{8}$')
        if com.match(phone):
            return phone
        raise forms.ValidationError('错误的手机号码')


class UserCommentForm(forms.Form):
    course = forms.IntegerField(required=True)
    content = forms.CharField(required=True, min_length=1, max_length=300)