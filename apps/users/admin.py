from django.contrib import admin


# Register your models here.
from users.models import UserProfile


class UserAdmin(admin.ModelAdmin):
    # 设置显示哪些字段
    list_display = ['pk', 'username', 'gender']
    # 添加搜索字段
    search_fields = ['username']


admin.site.register(UserProfile, UserAdmin)



