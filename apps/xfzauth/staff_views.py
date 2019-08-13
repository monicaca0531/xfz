# encoding: utf-8

from django.shortcuts import render,redirect,reverse
from .models import User
from django.views.generic import View
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from .decorators import xfz_superuser_require

@xfz_superuser_require
def staffs_view(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs':staffs
    }
    return render(request,'cms/staffs.html',context=context)

@method_decorator(xfz_superuser_require,name='dispatch')
class AddStaffs(View):
    def get(self,request):
        groups = Group.objects.all()
        context = {
            'groups':groups
        }
        return render(request,'cms/add_staff.html',context=context)

    def post(self,request):
        telephone = request.POST.get('telephone')
        print(telephone)
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            print(user.username)
            group_ids = request.POST.getlist('groups')
            groups = Group.objects.filter(pk__in=group_ids)
            user.groups.set(groups)
            user.save()
            return redirect(reverse('cms:staffs'))
        else:
            print('获取用户失败')
            return redirect(reverse('cms:staffs'))