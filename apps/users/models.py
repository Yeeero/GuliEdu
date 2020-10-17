from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.



class UserProfile(AbstractUser):
    image = models.ImageField(upload_to='users/', max_length=200, verbose_name='用户头像', null=True, blank=True)
    nick_name = models.CharField(max_length=20, verbose_name='用户昵称', null=True, blank=True)
    birthday = models.DateTimeField(verbose_name='用户生日', null=True, blank=True)
    gender = models.CharField(choices=(('female', '女'), ('male', '男')), max_length=10, verbose_name='用户性别')
    address = models.CharField(max_length=200, verbose_name='用户地址', null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name='用户手机', null=True, blank=True)
    is_status = models.BooleanField(default=False, verbose_name='是否已激活')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.username

    def get_msg_counter(self):
        '''

        :return: 返回用户未读消息数量
        '''
        from operations.models import UserMessage
        message_list = UserMessage.objects.filter(message_man=self.id, message_status=False)
        return message_list.count()


    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


# 轮播图信息表
class BannerInfo(models.Model):
    image = models.ImageField(upload_to='banner/', verbose_name='轮播图片', max_length=200)
    url = models.URLField(default='http://www.atguigu.com', max_length=200, verbose_name='轮播图片链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return str(self.image)

    class Meta:
        verbose_name = '轮播图信息'
        verbose_name_plural = verbose_name


# email验证码
class EmailVerifyCode(models.Model):
    code = models.CharField(max_length=20, verbose_name='邮箱验证码')
    email = models.EmailField(max_length=200, verbose_name='验证码邮箱')
    # 邮箱验证码类型，激活，遗忘，修改
    send_type = models.IntegerField(choices=((1, 'register'), (2, 'forget'), (3, 'change')), verbose_name='验证码类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '邮箱验证码信息'
        verbose_name_plural = verbose_name



