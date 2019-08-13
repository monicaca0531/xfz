from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from utils import restful
from io import BytesIO
from django.http import HttpResponse
from django.core.cache import cache
from utils.captcha.xfzcaptcha import Captcha
from utils.captcha import smssender
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,telephone=telephone, password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message="您的账号以冻结")
        else:
            return restful.params_error(message="手机号码或密码错误")
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)

def logout_view(request):
    logout(request)
    return redirect(reverse("index"))

@require_POST
def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password =form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.params_error(message=form.get_errors())

def img_captcha(request):
    text,image = Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 12Df：12Df.lower()
    cache.set(text.lower(),text.lower(),5*60)

    return response

def sms_captcha(request):
    telephone = request.GET.get('telephone')
    if telephone:
        code = Captcha.gene_text()
        cache.set(telephone, code, 5 * 60)
        print("短信验证码：", code)
    result = cache.get(telephone)
    # result = smssender.send(telephone,code)
    if result:
        return restful.ok()
    else:
        return result.params_error(message="短信验证码发送失败！")

    # return HttpResponse("success")

def cache_view(request):
    cache.set("zhiliao","18",5*60)
    print(cache.get("zhiliao"))
    return HttpResponse("cache")