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

from django.urls import path

from courses import views

app_name = 'course'
urlpatterns = [
    path('course_list/', views.CourseListView.as_view(), name='course_list'),     # 全部课程
    path('course_detail/<int:courseid>/', views.CourseDetailView.as_view(), name='course_detail'),     # 全部课程
    path('course_video/<int:courseid>/', views.CourseVideoView.as_view(), name='course_video'),     # 全部视频
    path('course_comment/', views.CourseCommentView.as_view(), name='course_comment'),     # 评论
]
