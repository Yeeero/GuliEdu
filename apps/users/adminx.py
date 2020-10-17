# -*- coding = utf-8 -*-
# @Time :
# @ Author : Yeeero
# @File : adminx.by
# @Software : PyCharm
import xadmin
from users.models import *


class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True
    model_icon = 'fa fa-gift'


class CommXadminSetting(object):
    site_title = '谷粒教育后台管理系统'
    site_footer = '尚硅谷it教育'
    menu_style = 'accordion'


class BannerInfoXadmin(object):
    list_display = ['image','url','add_time']
    search_fields = ['image', 'url']
    list_filter = ['image', 'url']


class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type','add_time']


xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode,EmailVerifyCodeXadmin)
# #注册主题类
# xadmin.site.register(views.BaseAdminView,BaseXadminSetting)
# #注册全局样式的类
# xadmin.site.register(views.CommAdminView,CommXadminSetting)