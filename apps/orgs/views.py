from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from users.views import login_status
# Create your views here.
from django.views.generic.base import View

from courses.models import CourseInfo
from operations.models import UserLove
from orgs.models import *


class OrgListView(View):
    def get(self, request):
        page = request.GET.get('page', 1)   # 当前页码
        orglist = OrgInfo.objects.all()     # 所有机构
        keywords = request.GET.get('keywords')
        print(f'{keywords=}')
        if keywords and keywords != 'None':
            orglist = orglist.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))      # search，模糊查询
        category = request.GET.get('ct')
        # 按机构类别进行分类查询
        if category and category != "None":
            orglist = orglist.filter(category=category)
        # 按在所在地区进行查询
        cityid = request.GET.get('cityid')
        if cityid and cityid != 'None':
            cityid = int(cityid)
            orglist = orglist.filter(cityyinfo_id=cityid)
        # 排序
        sort = request.GET.get('sort')
        if sort and sort != 'None':
            orglist = orglist.order_by('-'+sort)
        citylist = CityInfo.objects.all()
        sort_orgs = orglist.order_by('-love_num')
        paginator = Paginator(orglist, 1)
        org_page = paginator.page(int(page))
        return render(request, 'org-list.html', locals())


class OrgDetailView(View):  # 机构详情页
    @login_status
    def get(self, request, orgid=1):
        org = OrgInfo.objects.get(pk=orgid)
        org.click_num += 1
        org.save()
        # 判断该机构的收藏状态并返回
        love_status = '收藏'
        love = UserLove.objects.filter(love_user=request.user, love_id=orgid, love_type=1, love_status=True)
        if love:
            love_status = '取消收藏'
        return render(request, 'org-detail-homepage.html', locals())


class OrgDetailCourseView(View):
    def get(self, request, orgid):
        num = int(request.GET.get('page', 1))
        org = OrgInfo.objects.get(pk=orgid)
        courselist = org.courseinfo_set.all()
        paginator = Paginator(courselist, 4)
        course_page = paginator.page(num)
        active2 = 'course'
        # 判断该机构的收藏状态并返回
        love_status = '收藏'
        love = UserLove.objects.filter(love_user=request.user, love_id=orgid, love_type=1, love_status=True)
        if love:
            love_status = '取消收藏'
        return render(request, 'org-detail-course.html', locals())


class OrgDetailDescView(View):
    def get(self, request, orgid=None):
        org = OrgInfo.objects.get(pk=orgid)
        active2 = 'desc'
        # 判断该机构的收藏状态并返回
        love_status = '收藏'
        love = UserLove.objects.filter(love_user=request.user, love_id=orgid, love_type=1, love_status=True)
        if love:
            love_status = '取消收藏'
        return render(request, 'org-detail-desc.html', locals())


class OrgDetailTeacherView(View):
    def get(self, request, orgid=None):
        org = OrgInfo.objects.get(pk=orgid)
        active2 = 'teacher'
        # 判断该机构的收藏状态并返回
        love_status = '收藏'
        love = UserLove.objects.filter(love_user=request.user, love_id=orgid, love_type=1, love_status=True)
        if love:
            love_status = '取消收藏'
        return render(request, 'org-detail-teachers.html', locals())


class AddFavView(View):
    def get(self, request):
        obj = None
        print('start')
        love_id = int(request.GET.get('love_id'))
        love_type = int(request.GET.get('lovetype'))
        print(f'{love_type=},{love_id=}')
        if love_id and love_type:
            # 判断是否已经收藏,
            userloves = UserLove.objects.filter(love_id=love_id, love_type=love_type, love_user=request.user)
            # 根据love_type获取相应的对象
            if love_type == 1:
                obj = OrgInfo.objects.get(pk=love_id)
            if love_type == 2:
                obj = CourseInfo.objects.get(pk=love_id)
            if love_type == 3:
                obj = TeacherInfo.objects.get(pk=love_id)
            print(userloves)
            if userloves:
                # 如果收藏过，则取消收藏
                if userloves[0].love_status:
                    userloves[0].love_status = False
                    userloves[0].save()
                    obj.click_num -= 1
                    obj.save()
                    return JsonResponse({'msg': '收藏'})
                else:
                    userloves[0].love_status = True
                    userloves[0].save()
                    obj.click_num += 1
                    obj.save()
                    return JsonResponse({'msg': '取消收藏'})
            else:
                UserLove.objects.create(love_id=love_id, love_type=love_type, love_user=request.user)
                obj.click_num += 1
                obj.save()
                return JsonResponse({'msg': '取消收藏'})
        return JsonResponse({'msg': '收藏失败', 'status': 'fail'})


class TeacherListView(View):
    def get(self, request):
        teacher_list = TeacherInfo.objects.all()
        keywords = request.GET.get('keywords')
        if keywords and keywords != 'None':
            teacher_list = teacher_list.filter(name__icontains=keywords)
        sort = request.GET.get('sort')
        if sort == 'hot':
            teacher_list = teacher_list.order_by('-'+'love_num')
        paginator = Paginator(teacher_list, 2)
        page = int(request.GET.get('page', 1))
        teacher_page = paginator.page(page)
        # 热门讲师
        pop_teacher_list = teacher_list.order_by('-click_num')[:3]
        return render(request, 'teachers-list.html', locals())


class TeacherDetailView(View):
    @login_status
    def get(self, request, teacher_id):
        teacher = TeacherInfo.objects.get(pk=teacher_id)
        teacher.click_num += 1
        teacher.save()
        # 判断用户是否已收藏该讲师
        love_status = '取消收藏' if UserLove.objects.filter(love_user=request.user, love_id=teacher_id, love_type=3, love_status=True) else '收藏'
        # 讲师所属机构收藏状态
        org_id = teacher.work_company_id
        org_love_status = '取消收藏' if UserLove.objects.filter(love_user=request.user, love_id=org_id, love_type=1, love_status=True) else '收藏'
        pop_teacher_list = TeacherInfo.objects.order_by('-love_num')[:3]
        return render(request, 'teacher-detail.html', locals())