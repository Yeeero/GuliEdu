from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.template import loader


# Create your views here.
from django.views.generic.base import View

from GuliEdu import settings
from courses.models import CourseInfo
from operations.models import UserLove, UserCourse, UserMessage
from orgs.models import OrgInfo, TeacherInfo
from users.forms import *
from users.models import UserProfile
from utils.send_mail_tool import send_email_code
from utils.tools import token_confirm


class IndexView(View):
    def get(self, request):
        '''
        首页
        :param request:
        :return: index.html, 轮播图, 课程， 机构
        '''
        banner_list = BannerInfo.objects.order_by('-add_time')[:5]
        course_list = CourseInfo.objects.order_by('-love_num')[:8]
        org_list = OrgInfo.objects.all()[:15]
        return render(request, 'index.html', locals())


class Register(View):
    def get(self, request):
        register_form = UserRegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'register.html', {'msg': '用户名已存在', 'register_form': register_form})
            # user = UserProfile.objects.create(username=email, password=password)
            user = UserProfile()
            user.email = email
            user.username = email
            user.set_password(password)
            user.save()
            # send_email_code(email, 1)   # 1代表激活密码
            token = token_confirm.genenrate_valiable_token(user.id)
            print(token)
            # 构造验证的url
            url = "http://" + request.get_host() + reverse("users:active", kwargs={"token": token})
            # 加载模板
            html = loader.get_template('active.html').render({'url': url})
            print(url)
            send_mail("账号激活", '', settings.DEFAULT_FROM_EMAIL, [email], html_message=html)
            if user:
                return HttpResponse("账号注册成功，请到邮箱激活！")
        return render(request, 'register.html', {'register_form': register_form})


# 邮箱激活
class EmailActiveView(View):
    def get(self, request, token):
        # 邮件激活
        try:
            print('激活操作： token =', token)
            uid = token_confirm.confirm_valiable_token(token)
        except Exception as e:
            print(e)
            id = token_confirm.remove_valiable_token(token)
            user = UserProfile.objects.get(pk=id)
            user.delete()
            return HttpResponse("激活失败，请重新激活.")
        try:
            user = UserProfile.objects.get(pk=uid)
            user.is_status = True
            user.save()
        except:
            return HttpResponse("你激活的邮箱不存在，请重新注册！")
        return HttpResponse('邮件已激活')


class LoginView(View):
    def get(self, request):
        path = request.GET.get('path')
        return render(request, 'login.html', locals())

    def post(self, request, path=None):
        print(request.POST)
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print(f'{username=},{password=}')
            # user = UserProfile.objects.filter(Q(username=username) | Q(email=username) | Q(phone=username) & Q(password=password))
            user = authenticate(username=username, password=password)
            print(f'{user=}')
            if user:
                if user.is_status:
                    login(request, user)
                    # 登录成功后将登录消息保存到UserMessage中
                    usermessage = UserMessage()
                    usermessage.message_man = request.user.id
                    usermessage.message_content = 'Hello，{}欢迎来到尚硅谷教育网！'.format(request.user.nick_name)
                    usermessage.save()
                    path = request.POST.get('path')  # 获取登录跳转前页面的路径
                    # url = request.COOKIE.get('url', '/')  # 从cookie中获取保存的url
                    # ret = redirect('url')
                    # ret.delete_cookie('url')
                    # return ret
                    print(f"{path=}")
                    if path and path != 'None':
                        return redirect(path)  # 跳转回之前的页面
                    return redirect(reverse('index'))
                return HttpResponse("请激活你的邮箱再登录")
            return render(request, 'login.html', {'err': '用户名或密码错误'})
        return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class ForgetPwdView(View):
    def get(self, request):
        forget_form = UserForgetForm()
        return render(request, 'forgetpwd.html', locals())

    def post(self, request):
        forget_form = UserForgetForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            userlist = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            print(userlist)
            if userlist:
                token = token_confirm.genenrate_valiable_token(userlist[0].id)
                print(token)
                # 构造验证的url
                url = "http://" + request.get_host() + reverse("users:users_reset", kwargs={"token": token})
                # 加载模板
                html = loader.get_template('active.html').render({'url': url, 'send_type': 2})
                print(url)
                send_mail("账号激活", '', settings.DEFAULT_FROM_EMAIL, [email], html_message=html)
                return HttpResponse('重置密码')
            return render(request, 'forgetpwd.html', {'err': '该邮箱不存在', 'forget_form': forget_form})
        return render(request, 'forgetpwd.html', locals())


class UserResetView(View):      # 重置密码
    def get(self, request, token=None):

        return render(request, 'password_reset.html', locals())

    def post(self, request, token=None):
        user_reset_form = UserResetForm(request.POST)
        if user_reset_form.is_valid():
            password = user_reset_form.cleaned_data['password']
            password2 = user_reset_form.cleaned_data['password2']
            if password == password2:
                uid = token_confirm.confirm_valiable_token(token)
                user = UserProfile.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                return redirect(reverse('users:login'))
        return render(request, 'password_reset.html', {'msg': '密码输入不一致', 'token': token})


# 判断用户是否已登录，若没有登录，跳转到登录界面
def login_status(func):
        def inner(obj, request, *args, **kwargs):
            print(f'{request.user=},{request.path=}')
            if request.user.is_authenticated:
                return func(obj, request, *args, **kwargs)
            if request.is_ajax():   # 判断是否为ajax请求
                return JsonResponse({'status': 'nologin'})
            # 获取完整的url
            # url = request.get_full_path()
            # ret = redirect(reverse('users:login'))
            # ret.set_cookie('url', url)    # 将url保存到cookie中
            # return ret
            return redirect('/users/login/?path={}'.format(request.path))
        return inner


class UserCenterView(View):
    def get(self, request):
        user = request.user
        return render(request, 'usercenter-info.html', locals())

    def post(self, request):    # 修改用户信息
        print(request.POST)
        userinfo_form = UserChangeInfoForm(request.POST, instance=request.user)
        print(f'{userinfo_form.errors}')
        if userinfo_form.is_valid():
            userinfo_form.save(commit=True)
            return JsonResponse({'msg': 'success'})
        return JsonResponse({'msg': 'fail'})


class UserChangeImageView(View):        # ajax修改头像
    @login_status
    def post(self, request):
        # instance: 需要修改的实例对象;如果不指明，创建新的对象保存数据。
        image_change_form = UserChangeImageForm(request.POST, request.FILES, instance=request.user)
        if image_change_form.is_valid():
            print('======is_valid=====')
            image_change_form.save(commit=True)
            return JsonResponse({'msg': 'success'})
        return JsonResponse({'msg': 'fail'})


class SendEmailView(View):      # 发送修改邮箱验证码
    def get(self, request):
        email_form = UserChangeEmailForm(request.GET)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            users = UserProfile.objects.filter(Q(email=email)| Q(username=email))
            if users:
                return JsonResponse({'msg': '该邮箱已存在'})
            print(f'{email=}')
            # 查询该邮箱最近是否获取过验证码
            email_verf_list = EmailVerifyCode.objects.filter(email=email, send_type=3)
            if email_verf_list:
                email_verf = email_verf_list.order_by('-add_time')[0]
                if (datetime.now() - email_verf.add_time).seconds < 60:
                    return JsonResponse({'msg': '发送频率过高'})
                # 删除之前的验证码, 重新获取验证码
                email_verf.delete()
            send_email_code(email, 3)
            return JsonResponse({'msg': 'success'})
        return JsonResponse({'msg': 'fail'})


class UpdateEmailView(View):
    def post(self, request):
        email_form = UserChangeEmailForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            code = request.POST.get('code')
            emails = EmailVerifyCode.objects.filter(email=email, code=code)
            if emails:
                email_latest = emails.order_by('-add_time')[0]
                print((datetime.now() - email_latest.add_time).seconds)
                if (datetime.now() - email_latest.add_time).seconds > 300:
                    return JsonResponse({'status': '验证码已过期'})
                email_form.save(commit=True)
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'fail'})


class MyCourseView(View):  # 我的课程
    def get(self, request):
        '''
        我的课程展示页面
        :param request:
        :return: course_list,课程列表
        '''
        usercourse_list = request.user.usercourse_set.all()
        # usercourse_list = UserCourse.objects.filter(study_man=request.user)
        course_list = CourseInfo.objects.filter(pk__in=[usercourse.study_course.id for usercourse in usercourse_list])
        return render(request, 'usercenter-mycourse.html', locals())


class FavCourseView(View):
    def get(self, request):
        course_list = CourseInfo.objects.filter(pk__in=[userlove.love_id for userlove in UserLove.objects.filter(love_user=request.user, love_type=2, love_status=True)])   # 收藏的课程
        org_list = OrgInfo.objects.filter(pk__in=[userlove.love_id for userlove in UserLove.objects.filter(love_user=request.user, love_type=1, love_status=True)])    # 收藏的机构
        teacher_list = TeacherInfo.objects.filter(pk__in=[userlove.love_id for userlove in UserLove.objects.filter(love_user=request.user, love_type=3, love_status=True)])     # 收藏的老师
        print(course_list)
        return render(request, 'usercenter-fav-course.html', locals())


class MessageView(View):
    def get(self, request):
        '''
        返回用户消息记录
        :param request:
        :return: message_list
        '''
        usermessage_list = UserMessage.objects.filter(message_man=request.user.id).order_by('-add_time')
        paginator = Paginator(usermessage_list, 2)
        page_num = request.GET.get('page', 1)
        meg_page = paginator.page(page_num)
        return render(request, 'usercenter-message.html', locals())


def handler_404(request, exception):
    print('handler 404')
    return render(request, 'handler_404.html')


def handler_500(request, exception):
    print('handler 404')
    return render(request, 'handler_500.html')