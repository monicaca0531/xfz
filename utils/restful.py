# encoding: utf-8

from django.http import JsonResponse

class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    severerror = 500

def result(code=HttpCode.ok,message="",data=None,kwargs=None):
    json_dict = {"code":code, "message":message, "data":data}

    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)

def ok():
    return result()

def params_error(message="",data=""):
    return result(code=HttpCode.paramserror, message=message, data=data)

def unauth(message="",data=""):
    return result(code=HttpCode.unauth,message=message,data=data)

def method_error(message="",data=""):
    return result(code=HttpCode.methoderror, message=message, data=data)

def server_error(message="",data=""):
    return result(code=HttpCode.severerror, message=message, data=data)