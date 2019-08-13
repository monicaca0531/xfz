# encoding: utf-8

from utils import restful
from django.shortcuts import redirect
from functools import wraps
from django.http import Http404

def xfz_login_require(func):
    def wraper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message="请先登录！")
            else:
                return redirect('/')
    return wraper

def xfz_superuser_require(viewfun):
    @wraps(viewfun)
    def decorator(request,*args,**kwargs):
        if request.user.is_superuser:
            return viewfun(request,*args,**kwargs)
        else:
            raise Http404
    return decorator