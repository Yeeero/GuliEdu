# -*- coding = utf-8 -*-
# @Time :
# @ Author : Yeeero
# @File : myfilter.by
# @Software : PyCharm
from django import template

register = template.Library()


@register.filter(name='percent')
def percent(value):
    return value + "%"