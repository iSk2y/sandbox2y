#!/usr/bin/env python
# -*- coding:utf-8 -*-
#    @Author:iSk2y

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import LoginForm
from .mixin import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    """
    index视图类
    """
    def get(self, request):
        print('index')
        return render(request, 'index.html')


class LoginView(View):
    """
    用户登录视图
    """
    def get(self, request):
        if not request.user.is_authenticated:
            # 认证失败 转向登录页面
            return render(request, 'system/users/login.html')
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        redirect_to = request.GET.get('next', '/')
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            user_name = login_form.cleaned_data.get("username")
            pass_word = login_form.cleaned_data.get("password")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 是否已经激活
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    ret['msg'] = '用户未激活！'
            else:
                ret['msg'] = '用户名或密码错误！'
        else:
            ret['msg'] = ['用户名密码不能为空！']
        return render(request, 'system/users/login.html', ret)


class LogoutView(View):
    """
    登出视图
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))