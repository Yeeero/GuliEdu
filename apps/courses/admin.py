from django.contrib import admin

# Register your models here.
from courses.models import CourseInfo


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(CourseInfo, CourseAdmin)