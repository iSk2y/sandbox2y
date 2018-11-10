#!/usr/bin/env python
# -*- coding:utf-8 -*-
#    @Author:iSk2y

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"requeired": "请填写用户名"})
    password = forms.CharField(required=True, error_messages={"requeired": "请填写密码"})
