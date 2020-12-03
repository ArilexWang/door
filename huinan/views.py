from huinan.models import Member
from rest_framework import generics, renderers, permissions, viewsets
from huinan.serializers import MemberSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import requests
import time
import json
import hashlib
import base64
from huinan.WXBizDataCrypt import WXBizDataCrypt

appid = "wx0254886385e4f4ae"
appSecret = "5af956969ca1728dd53b0f32b6df4c13"
wechatUrl = 'https://api.weixin.qq.com/sns/jscode2session'
funcUrl = 'https://api.weixin.qq.com/tcb/invokecloudfunction'
tokenUrl = 'https://api.weixin.qq.com/cgi-bin/token'
env = 'test-3gyot3qv80f8b08e'
exp_time = 0
access_token = ''


@api_view(['GET'])
def echo(request):
    if request.method == 'GET':
        token = get_access_token()
        r = requests.post(funcUrl, params={
                          'access_token': token, 'env': env, 'name': 'echo'}, data=json.dumps({"ab": "fuck"}))
        print(r.url)
        return Response(r.json())


def heartbeat(request):
    if request.method == 'GET':
        key = request.GET.get('Key')
        result = "DATA={\"Key\":\"" + key + "\"}"
        return HttpResponse(result)


def checkCode(request):
    if request.method == 'GET':
        code64 = request.GET.get('Card')
        if (code64 == '0004267148'):
            res = "DATA={\"ActIndex\":\"" + "1" + \
                "\",\"AcsRes\":\""+"1"+"\",\"Time\":\""+"1"+"\"}"
            return HttpResponse(res)
        else:
            codeStr = decode64(code64)
            reader = request.GET.get('Reader')
            token = get_access_token()
            r = requests.post(funcUrl, params={
                'access_token': token, 'env': env, 'name': 'checkCode'}, data=json.dumps({"code": codeStr, "reader": reader}))
            result = json.loads(r.text)
            if result['resp_data'] == 'true':
                acsRes = "1"
            else:
                acsRes = "0"
            actIndex = reader
            time = "1"
            res = "DATA={\"ActIndex\":\"" + actIndex + \
                "\",\"AcsRes\":\""+acsRes+"\",\"Time\":\""+time + \
                "\",\"Voice\":\"欢迎光临\",\"Note\":\"扫码入场\",\"Name\":\"张三\"}"
            print(res.encode('gb2312'))
            return HttpResponse(res.encode('gb2312'), content_type='text/html;charset=gbk')


def get_access_token():
    global exp_time, access_token
    print(exp_time)
    if time.time() > exp_time:
        r = requests.get(tokenUrl, {
                         'grant_type': 'client_credential', 'appid': appid, 'secret': appSecret})
        d = json.loads(r.text)
        access_token = d['access_token']
        exp_time = time.time() + d['expires_in'] - 10
    return access_token


def decode64(str):
    str.replace(' ', '+')
    str.replace('-', '+')
    str.replace('_', '/')
    if (len(str) % 4 == 2):
        str += '=='
    if (len(str) % 4 == 3):
        str += '='
    code = base64.b64decode(str)
    return bytes.decode(code)
