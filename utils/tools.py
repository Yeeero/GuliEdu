# -*- coding = utf-8 -*-
# @Time :
# @ Author : Yeeero
# @File : tools.by
# @Software : PyCharm

# 邮件验证的类
import base64
from itsdangerous import URLSafeSerializer as utsr
from django.conf import settings as django_settings


class Token:
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode('utf-8'))

    # 生成token
    def genenrate_valiable_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    # 验证token
    def confirm_valiable_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)

    # 移除token
    def remove_valiable_token(self, token):
        serializer = utsr(self.security_key)
        print(serializer.loads(token, self.salt))
        return serializer.loads(token, salt=self.salt)


token_confirm = Token(django_settings.SECRET_KEY)        # 定义为全局变量