# -*- coding = utf-8 -*-
# @Time :
# @ Author : Yeeero
# @File : send_mail_tool.by
# @Software : PyCharm
from django.core.mail import send_mail
from django.template import loader
from random import randrange

from GuliEdu import settings
from users.models import EmailVerifyCode
from utils.tools import token_confirm

def get_ramdon_code(code_length=6):
    code_source ='0123456789'
    code = ''
    for i in range(0, code_length):
        # 随机一个字符
        code += code_source[randrange(0, len(code_source))]
    return code


def send_email_code(email, send_type):
    #1 创建邮箱验证码对象，保存数据库
    code = get_ramdon_code(6)

    e = EmailVerifyCode()
    e.email = email
    e.send_type = send_type
    e.code = code
    e.save()    # 保存验证码到数据库

    #第二步：正式的发邮件功能
    if send_type == 3:      # 修改邮箱
        send_title = '修改邮箱验证码'
        send_body = '你的验证码是' + code
        send_mail(send_title, send_body, settings.DEFAULT_FROM_EMAIL, [email])
