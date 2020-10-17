from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from operations.forms import UserAskForm


class UserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        print(user_ask_form.is_valid())
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return JsonResponse({'status': 'ok', 'msg': '咨询成功'})
        print(dict(user_ask_form.errors.items()))
        return JsonResponse({'status': 'fail', 'msg': '咨询失败', 'err': dict(user_ask_form.errors.items())})
