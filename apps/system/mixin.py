#!/usr/bin/env python
# -*- coding:utf-8 -*-
#    @Author:iSk2y


from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """
    登录装饰器
    """
    @classmethod
    def as_view(cls, **init_kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**init_kwargs)
        return login_required(view)