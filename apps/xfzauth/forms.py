# encoding: utf-8

from django import forms
from django.core.cache import cache
from apps.forms import FormMixin
from .models import User

class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,error_messages={"max_length":"手机号码为11位"})
    password = forms.CharField(max_length=20,min_length=6,error_messages={"max_length":"密码最多不能超过20位！",
                                                                          "min_length":"密码最少需要6位！"})
    remember = forms.IntegerField(required=False)

class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20, min_length=6, error_messages={"max_length": "密码最多不能超过20位！",
                                                                            "min_length": "密码最少需要6位！"})
    password2 = forms.CharField(max_length=20, min_length=6, error_messages={"max_length": "密码最多不能超过20位！",
                                                                             "min_length": "密码最少需要6位！"})
    img_captcha = forms.CharField(max_length=4,min_length=4)
    sms_captcha = forms.CharField(max_length=4,min_length=4)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("两次密码输入不一致")

        img_captcha = cleaned_data.get('img_captcha')
        cache_img_captcha = cache.get(img_captcha.lower())
        if not cache_img_captcha or img_captcha.lower() != cache_img_captcha.lower():
            raise forms.ValidationError("验证码输入错误！")

        sms_captcha = cleaned_data.get('sms_captcha')
        telephone = cleaned_data.get('telephone')
        cache_sms_captcha = cache.get(telephone)
        if not cache_sms_captcha or cache_sms_captcha != sms_captcha:
            raise forms.ValidationError("短信验证码输入错误！")

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError("该手机号码已被注册！")

        return cleaned_data