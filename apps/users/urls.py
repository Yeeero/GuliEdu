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

from users import views

app_name = 'users'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/', views.IndexView.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('active/<token>/', views.EmailActiveView.as_view(), name='active'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('forgetpwd/', views.ForgetPwdView.as_view(), name='forgetpwd'),
    path('users_reset/<token>/', views.UserResetView.as_view(), name='users_reset'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('usercenter/', views.UserCenterView.as_view(), name='usercenter'),     # 用户中心
    path('userchangeimage/', views.UserChangeImageView.as_view(), name='userchangeimage'),     # 头像修改
    path('sendemail_code/', views.SendEmailView.as_view(), name='sendemail_code'),     # 发送邮箱验证码
    path('update_email/', views.UpdateEmailView.as_view(), name='update_email'),     # 修改邮箱
    path('mycourse/', views.MyCourseView.as_view(), name='mycourse'),     # 我的课程
    path('fav_course/', views.FavCourseView.as_view(), name='fav_course'),     # 我的收藏
    path('message/', views.MessageView.as_view(), name='message'),     # 我的消息

]


