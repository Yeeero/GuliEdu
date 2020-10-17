from django.contrib import admin


# Register your models here.
from orgs.models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ['name']


class OrgAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'course_num', 'study_num', 'love_num', 'click_num', 'category', 'cityinfo']
    style_fields = {'detail': 'ueditor'}

class TeacherAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 5
    # 过滤字段
    list_filter = ['name']
    list_display = ['image', 'name', 'work_year', 'work_company', 'gender']


admin.site.register(CityInfo, CityAdmin)
admin.site.register(TeacherInfo, TeacherAdmin)
admin.site.register(OrgInfo, OrgAdmin)