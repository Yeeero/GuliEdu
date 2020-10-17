from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.views.generic.base import View

from courses.models import *
from operations.forms import UserCommentForm
from operations.models import UserLove, UserCourse, UserComment
from users.views import login_status


class CourseListView(View):
    def get(self, request):
        course_list = CourseInfo.objects.all()
        keywords = request.GET.get('keywords')
        print(f'{keywords=}')
        if keywords and keywords != 'None':
            course_list = course_list.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))
        recommend_course_list = course_list.order_by('-add_time')[:3]   # 热门推荐
        # 排序
        sort = request.GET.get('sort')
        print(f'{sort=}')
        if sort and sort != 'None' and sort != '':
            course_list = course_list.order_by('-' + sort)
        paginator = Paginator(course_list, 2)
        page_num = int(request.GET.get('page_num', 1))
        course_page = paginator.page(page_num)
        return render(request, 'course-list.html', locals())


class CourseDetailView(View):   # 课程详情
    @login_status
    def get(self, request, courseid=1):
        course = CourseInfo.objects.get(pk=courseid)
        course.click_num += 1
        course.save()
        # 相关课程
        relate_course = CourseInfo.objects.filter(category=course.category).exclude(pk=courseid)[:3]
        # 机构收藏状态
        love_status = '取消收藏' if UserLove.objects.filter(love_user=request.user, love_id=course.orginfo.id, love_type=1, love_status=True) else '收藏'
        # 课程收藏状态
        love_course_status = '取消收藏' if UserLove.objects.filter(love_user=request.user, love_id=course.id, love_type=2, love_status=True) else '收藏'
        return render(request, 'course-detail.html', locals())


class CourseVideoView(View):    # 开始学习
    @login_status
    def get(self, request, courseid):
        course = CourseInfo.objects.get(pk=courseid)
        try:
            usercourses = UserCourse.objects.get(study_man=request.user, study_course=course)
            print(f'{usercourses=}')
        except Exception:
            UserCourse.objects.create(study_man=request.user, study_course_id=courseid)
            # 学习该课程人数+1
            course.study_num += 1
            course.orginfo.study_num += 1
            course.save()
        # 学过该课的同学还学过的课程
        # other_course = UserCourse.objects.filter(study_man=request.user).exclude(study_course=course)
        usercourse_list = UserCourse.objects.filter(study_course=course)
        user_list = [user.study_man for user in usercourse_list]
        other_course = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course).distinct()[:3]
        # 用户评论
        comment_list = UserComment.objects.filter(comment_course=course).order_by('add_time')[:10]
        return render(request, 'course-video.html', locals())


class CourseCommentView(View):  # 发表评论

    def post(self, request):
        # user_comment_form = UserCommentForm(request.POST)
        print('-------comment add------')
        content = request.POST.get('comments')
        courseid = request.POST.get('courseid')
        comment = UserComment.objects.create(comment_course_id=courseid, comment_content=content, comment_man=request.user)
        if comment:
            return JsonResponse({'msg': 'success'})
        return JsonResponse({'msg': 'fail'})


