from django.shortcuts import render
import random
from django.http import HttpResponse,JsonResponse
from datetime import datetime   #时间函数
import json
import requests
import hashlib
from .models import *       #User Album
from django_redis import get_redis_connection   #连接redis
from .serializers import UserSerializer
from .openid import OpenId      #获取openid的类
import time
import os
from .forms import UploadFileForm
from .py_scripts import scripts_findlostpeople
from rest_framework.decorators import api_view, authentication_classes

def findlostpeople(request):
    if request.method == "POST":
        print("request POST:", request.POST)
        print("request FILE:", request.FILES)  # official page 1301
        print("request FILE DETAIL:", request.FILES['portrait'])  # 传递过来的name参数中是什么就用什么来访问，这里测试的是file-name
        ### 存储传过来的图片
        ### 存储到./picture-temp/request.FILES['portrait']
        THIS_FILE_PATH = './picture-temp/' + str(request.FILES['portrait'])
        with open(THIS_FILE_PATH,'wb+') as destination:
            for chunk in request.FILES['portrait'].chunks():
                destination.write(chunk)

        ###调用自定义API
        findpeople_api_return = scripts_findlostpeople.get_xunqinweb(THIS_FILE_PATH)
        print("自定义API调用完毕")
        os.remove(THIS_FILE_PATH)
        if findpeople_api_return == "not find":
            return JsonResponse({"status":False,"datalist":""})
        return JsonResponse({"status":True,"datalist":findpeople_api_return})

@authentication_classes([])  # 添加
def onLogin(request):           #响应微信用户登录中wx.login中后来的request
    if request.method == 'POST':
        js_code = request.POST.get('code','')
        ###获取用户的openid 和 session key
        openid_return = OpenId(js_code).get_openid()
        if openid_return=='fail':
            print("获取Openid和session_key失败")
        else:
            openid, session_key = openid_return

        #登录成功
        print('登录成功')
        user, created = User.objects.get_or_create(openid=openid)
        user_str = str(UserSerializer(user).data)   #获取用户表项对应的序列化对象
        print("user:{0},created:{1}".format(user,created))
        # 生成自定义登录态，返回给前端
        sha = hashlib.sha1()
        sha.update(openid.encode())
        sha.update(session_key.encode())
        digest = sha.hexdigest()
        conn = get_redis_connection('default')
        conn.set(digest, user_str, ex=2 * 60 * 60)
        #   返回对应的数据
        return HttpResponse({'secretkey': digest})

@authentication_classes([])  # 添加
def album(request):
    if request.method == 'POST':         #创建相册请求
        nickname = request.POST.get('nickname', '').encode()
        albumname = request.POST.get('albumname', '')
        visibility = True if request.POST.get('visibility', '')=="true" else False
        createtime = request.POST.get('createtime', '')
        if Album.objects.filter(albumname=albumname):
            print("相册重复创建")
            response =  JsonResponse({'status': '相册重复创建'})
            response.status_code = 400
            return response
        newAlbum = Album(nickname=nickname,albumname=albumname,visibility=visibility,createtime=createtime,totalsum=0)
        newAlbum.save()
        print("上传相册信息完成，已经存储",Album.objects.all())
        return JsonResponse({'status':'success'})

    if request.method == "GET":      #刷新相册请求
        nickname = request.GET.get('nickname','').encode()  #得到相册中该用户的信息
        if 'albumname' in request.GET:
            print("跳转到albumdetail")
            albumname = request.GET.get('albumname','')
            exact_item = Album.objects.filter(nickname=nickname,albumname=albumname)[0]
            res = {
                    "albumname": albumname,
                    "visibility": exact_item.visibility,
                    "createtime": str(exact_item.createtime)[:10],
                    "totalsum": exact_item.totalsum
                }
            return JsonResponse(res, safe=False)

        array_return = []
        for i,item in enumerate(Album.objects.filter(nickname=nickname)):
            current_color = ['lightgray','lightgreen','lightblue']
            array_return.append({
                "albumname":item.albumname,
                "visibility": item.visibility,
                "createtime": str(item.createtime)[:10],
                "backgroundcolor":current_color[random.randint(0,len(current_color)-1)],
                "totalsum": item.totalsum
            })
        return JsonResponse(array_return,safe=False)

@authentication_classes([])
def albumdetail(request):
    pass