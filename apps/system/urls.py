#!/usr/bin/env python
# -*- coding:utf-8 -*-
#    @Author:iSk2y

from django.urls import path

from .views import SystemView
from . import views_structure

app_name = 'system'

urlpatterns = [
    path('', SystemView.as_view(), name='login'),
    path('basic/structure/', views_structure.StructureView.as_view(), name='basic_structure'),
    path('basic/structure/create/', views_structure.StructureCreateView.as_view(), name='basic_structure_create'),
    path('basic/structure/list/', views_structure.StructureListView.as_view(), name='basic_structure_list'),
    path('basic/structure/delete/', views_structure.StructureDeleteView.as_view(), name='basic_structure_delete'),
    path('basic/structure/add_user/', views_structure.Structure2UserView.as_view(), name='basic_structure_add_user'),
]