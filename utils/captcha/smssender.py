# encoding: utf-8

import requests

def send(mobile,captcha):
    url = 'http://v.juhe.cn/sms/send'
    params = {
        'mobile': mobile,
        'tpl_id': '176407',
        'tpl_value': "#code#="+captcha,
        'key': 'bea49891fc6a193bb8dbef3469419311',
    }
    response = requests.get(url,params=params)
    result = response.json()
    if result['error_code'] == 0:
        return True
    else:
        return False