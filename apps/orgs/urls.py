"""GuliEdu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from orgs import views

app_name = 'orgs'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('orglist/', views.OrgListView.as_view(), name='orglist'),      # 授课机构列表
    path('org_detail/', views.OrgDetailView.as_view(), name='org_detail'),
    path('org_detail/<int:orgid>/', views.OrgDetailView.as_view(), name='org_detail'),  # 机构首页
    path('org_detail_course/', views.OrgDetailCourseView.as_view(), name='org_detail_course'),      # 机构课程
    path('org_detail_course/<int:orgid>/', views.OrgDetailCourseView.as_view(), name='org_detail_course'),
    # path('org_detail_desc/', views.OrgDetailDescView.as_view(), name='org_detail_desc'),    # 机构介绍
    path('org_detail_desc/<int:orgid>/', views.OrgDetailDescView.as_view(), name='org_detail_desc'),
    # path('org_detail_teacher/', views.OrgDetailTeacherView.as_view(), name='org_detail_teacher'),   # 机构讲师
    path('org_detail_teacher/<int:orgid>/', views.OrgDetailTeacherView.as_view(), name='org_detail_teacher'),
    path('add_fav/', views.AddFavView.as_view(), name='add_fav'),   # 点击收藏
    path('teacher_list/', views.TeacherListView.as_view(), name='teacher_list'),   # 讲师列表页面
    path('teacher_detail/<int:teacher_id>/', views.TeacherDetailView.as_view(), name='teacher_detail'),   # 讲师列表页面.
]