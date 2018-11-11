#!/usr/bin/env python
# -*- coding:utf-8 -*-
#    @Author:iSk2y

from django.urls import path

from .views import SystemView

app_name = 'system'

urlpatterns = [
    path('', SystemView.as_view(), name='login'),
]