#!/usr/bin/env python
# -*- coding:utf-8 -*-
#    @Author:iSk2y
import json
import re
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.db.models import Q
from django.views.generic.base import View, TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from .forms import LoginForm, UserCreateForm, UserUpdateForm, PasswordChangeForm
from .models import Structure, Role
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


User = get_user_model()


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'system/users/user.html'


class UserListView(LoginRequiredMixin, View):
    """
    用户列表视图
    """

    def get(self, request):
        fields = ['id', 'name', 'gender', 'mobile', 'email', 'department__name', 'post', 'superior__name', 'is_active']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['is_active'] = request.GET['select']
        ret = dict(data=list(User.objects.filter(**filters).values(*fields)))
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserCreateView(LoginRequiredMixin, View):
    """
    创建用户视图
    """
    def get(self, request):
        users = User.objects.exclude(username='admin')
        structures = Structure.objects.values()
        roles = Role.objects.values()

        ret = {
            'users': users,
            'structures': structures,
            'roles': roles,
        }
        return render(request, 'system/users/user_create.html', ret)

    def post(self, request):
        user_create_form = UserCreateForm(request.POST)
        if user_create_form.is_valid():
            new_user = user_create_form.save(commit=False)
            new_user.password = make_password(user_create_form.cleaned_data['password'])
            new_user.save()
            user_create_form.save_m2m()
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(user_create_form.errors)
            user_create_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'user_create_form_errors': user_create_form_errors[0]
            }
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDetailView(LoginRequiredMixin, View):
    """
    用户详情视图
    """

    def get(self, request):
        user = get_object_or_404(User, pk=int(request.GET['id']))
        users = User.objects.exclude(Q(id=int(request.GET['id'])) | Q(username='admin'))
        structures = Structure.objects.values()
        roles = Role.objects.values()
        user_roles = user.roles.values()
        ret = {
            'user': user,
            'structures': structures,
            'users': users,
            'roles': roles,
            'user_roles': user_roles
        }
        return render(request, 'system/users/user_detail.html', ret)


class UserUpdateView(LoginRequiredMixin, View):

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
        else:
            user = get_object_or_404(User, pk=int(request.user.id))
        user_update_form = UserUpdateForm(request.POST, instance=user)
        if user_update_form.is_valid():
            user_update_form.save()
            ret = {"status": "success"}
        else:
            ret = {"status": "fail", "message": user_update_form.errors}
        return HttpResponse(json.dumps(ret), content_type="application/json")


class PasswordChangeView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            user = get_object_or_404(User, pk=int(request.GET.get('id')))
            ret['user'] = user
        return render(request, 'system/users/passwd_change.html', ret)

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
            form = PasswordChangeForm(request.POST)
            if form.is_valid():
                new_password = request.POST['password']
                user.set_password(new_password)
                user.save()
                ret = {'status': 'success'}
            else:
                pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
                errors = str(form.errors)
                password_change_form_errors = re.findall(pattern, errors)
                ret = {
                    'status': 'fail',
                    'password_change_form_errors': password_change_form_errors[0]
                }
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDeleteView(LoginRequiredMixin, View):
    """
    删除数据：支持删除单条记录和批量删除
    """

    def post(self, request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            User.objects.filter(id__in=id_list).delete()
            ret['result'] = True
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserEnableView(LoginRequiredMixin, View):
    """
    启用用户：单个或批量启用
    """

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = User.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=False).update(is_active=True)
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')


class UserDisableView(LoginRequiredMixin, View):
    """
   禁用用户：单个或批量禁用
    """

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            id_nums = request.POST.get('id')
            queryset = User.objects.extra(where=["id IN(" + id_nums + ")"])
            queryset.filter(is_active=True).update(is_active=False)
            ret = {'result': 'True'}
        return HttpResponse(json.dumps(ret), content_type='application/json')