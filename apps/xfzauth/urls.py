# encoding: utf-8

from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.register_view,name='register'),
    path('img_captcha/',views.img_captcha,name='img_captcha'),
    path('sms_captcha/',views.sms_captcha,name='sms_captcha'),
    path('cache/',views.cache_view,name='cache'),
]