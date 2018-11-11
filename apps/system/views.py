from django.shortcuts import render
from django.views.generic.base import View, TemplateView

from .mixin import LoginRequiredMixin


class SystemView(LoginRequiredMixin, TemplateView):
    """
    继承自TemplateView，无需创建get方法，只要修改模板名字
    Template -> View
    """
    template_name = 'system/system_index.html'
