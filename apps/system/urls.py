#!/usr/bin/env python
# -*- coding:utf-8 -*-
#    @Author:iSk2y

from django.urls import path

from .views import SystemView
from . import views_user
from . import views_structure

app_name = 'system'

urlpatterns = [
    path('', SystemView.as_view(), name='login'),
    path('basic/structure/', views_structure.StructureView.as_view(), name='basic_structure'),
    path('basic/structure/create/', views_structure.StructureCreateView.as_view(), name='basic_structure_create'),
    path('basic/structure/list/', views_structure.StructureListView.as_view(), name='basic_structure_list'),
    path('basic/structure/delete/', views_structure.StructureDeleteView.as_view(), name='basic_structure_delete'),
    path('basic/structure/add_user/', views_structure.Structure2UserView.as_view(), name='basic_structure_add_user'),
    path('basic/user/', views_user.UserView.as_view(), name='basic_user'),
    path('basic/user/list/', views_user.UserListView.as_view(), name='basic_user_list'),
    path('basic/user/create/', views_user.UserCreateView.as_view(), name='basic_user_create'),
    path('basic/user/detail/', views_user.UserDetailView.as_view(), name='basic_user_detail'),
    path('basic/user/update/', views_user.UserUpdateView.as_view(), name='basic_user_update'),
    path('basic/user/password_change/', views_user.PasswordChangeView.as_view(), name='basic_user_password_change'),
    path('basic/user/delete/', views_user.UserDeleteView.as_view(), name='basic_user_delete'),
    path('basic/user/enable/', views_user.UserEnableView.as_view(), name='basic_user_enable'),
    path('basic/user/disable/', views_user.UserDisableView.as_view(), name='basic_user_disable'),
]