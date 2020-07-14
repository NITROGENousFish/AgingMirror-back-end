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
from .py_scripts import tencent_faceaging
from rest_framework.decorators import api_view, authentication_classes
from django.http import QueryDict
import base64


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

def crossagecomparation(request):
    PIC_FOLDER = './faceaging/py_scripts/crossagecomparation/'
    if request.method == "POST":
        if 'pic' in request.POST:  # 说明是上传图片的请求,pic中如果是0就是1号图片，是1就是2号图
            print("收到PIC")
            PIC_ID = request.POST.get('pic', '')
            nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")
            serverUrl = PIC_ID+"_"+nickname+"_"+str(request.FILES['crossagecomparation'])
            THIS_FILE_PATH = PIC_FOLDER + serverUrl
            with open(THIS_FILE_PATH, 'wb+') as destination:
                for chunk in request.FILES['crossagecomparation'].chunks():
                    destination.write(chunk)
            return JsonResponse({'serverUrl':serverUrl})
        if 'image1path' in request.POST:  # 说明是开始处理的的请求
            image0path = request.POST.get('image0path', '')
            image1path = request.POST.get('image1path', '')
            rate = tencent_faceaging.processFaceagingPicture(PIC_FOLDER+image0path,PIC_FOLDER+image1path)
            image0path_base64_data = base64.b64encode(open(PIC_FOLDER+image0path, 'rb') .read()).decode()
            image1path_base64_data = base64.b64encode(open(PIC_FOLDER+image1path, 'rb') .read()).decode()
            os.remove(PIC_FOLDER+image0path)
            os.remove(PIC_FOLDER + image1path)
            return JsonResponse({
                "rate":rate,
                "url1":'data:image/png;base64,'+image0path_base64_data,
                "url2":'data:image/png;base64,'+image1path_base64_data
            })

def styletransfer(request):
    PIC_FOLDER = './faceaging/py_scripts/styletransfer/'
    STYLETRANSFER_SERVER_URL = 'http://127.0.0.1:8001/show/'
    if request.method == "POST":
        if 'pic' in request.POST:  # 说明是上传图片的请求,pic中如果是0就是1号图片，是1就是2号图
            print("收到PIC")
            PIC_ID = request.POST.get('pic', '')
            nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")
            serverUrl = PIC_ID+"_"+nickname+"_"+str(request.FILES['styletransfer'])
            THIS_FILE_PATH = PIC_FOLDER + serverUrl
            with open(THIS_FILE_PATH, 'wb+') as destination:
                for chunk in request.FILES['styletransfer'].chunks():
                    destination.write(chunk)
            return JsonResponse({'serverUrl':serverUrl})
        if 'image1path' in request.POST:  # 说明是开始处理的的请求
            image0path = request.POST.get('image0path', '')
            image1path = request.POST.get('image1path', '')
            nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")
            print(PIC_FOLDER+image0path)
            files = {
                "content_img":(image0path,open(PIC_FOLDER+image0path,'rb'),'image/png',{}),
                "style_img": (image1path, open(PIC_FOLDER + image1path, 'rb'), 'image/png', {}),
            }

            try:
                res = requests.post(STYLETRANSFER_SERVER_URL,data={"id":nickname},files=files)
                image0path_base64_data = res.text
                return JsonResponse({
                    "url":'data:image/png;base64,'+image0path_base64_data,
                })
            except:
                response =  JsonResponse({'status': '风格迁移服务器未工作'})
                response.status_code = 400
                return response

def agedetection(request):
    STYLETRANSFER_SERVER_URL = 'http://127.0.0.1:8002/show/'
    PIC_FOLDER = './faceaging/py_scripts/agedetection/'
    if request.method == "POST":
        if 'pic' in request.POST:  # 说明是上传图片的请求,pic中如果是0就是1号图片，是1就是2号图
            print("收到PIC")
            PIC_ID = request.POST.get('pic', '')
            nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")
            serverUrl = PIC_ID+"_"+nickname+"_"+str(request.FILES['agedetection'])
            THIS_FILE_PATH = PIC_FOLDER + serverUrl
            with open(THIS_FILE_PATH, 'wb+') as destination:
                for chunk in request.FILES['agedetection'].chunks():
                    destination.write(chunk)
            return JsonResponse({'serverUrl':serverUrl})
    if 'image1path' in request.POST:  # 说明是开始处理的的请求

        image1path = request.POST.get('image1path', '')
        nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")

        files = {
            "image": (image1path, open(PIC_FOLDER + image1path, 'rb'), 'image/png', {}),
        }
        res = requests.post(STYLETRANSFER_SERVER_URL, data={"id": nickname}, files=files)
        # print(res.text)
        return JsonResponse(res.text,safe=False)
        # try:
        #
        #
        #     return JsonResponse(res.text)
        # except:
        #     response = JsonResponse({'status': '颜龄检测服务器未工作'})
        #     response.status_code = 400
        #     return response

def wrinkleadd(request):
    STYLETRANSFER_SERVER_URL = 'http://127.0.0.1:8003/show/'
    PIC_FOLDER = './faceaging/py_scripts/agedetection/'
    if request.method == "POST":
        if 'pic' in request.POST:  # 说明是上传图片的请求,pic中如果是0就是1号图片，是1就是2号图
            print("收到PIC")
            PIC_ID = request.POST.get('pic', '')
            nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")
            serverUrl = PIC_ID+"_"+nickname+"_"+str(request.FILES['wrinkleadd'])
            THIS_FILE_PATH = PIC_FOLDER + serverUrl
            with open(THIS_FILE_PATH, 'wb+') as destination:
                for chunk in request.FILES['wrinkleadd'].chunks():
                    destination.write(chunk)
            return JsonResponse({'serverUrl':serverUrl})
    if 'image1path' in request.POST:  # 说明是开始处理的的请求

        image1path = request.POST.get('image1path', '')
        nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")

        files = {
            "image": (image1path, open(PIC_FOLDER + image1path, 'rb'), 'image/png', {}),
        }
        res = requests.post(STYLETRANSFER_SERVER_URL, data={"id": nickname}, files=files)
        # print(res.text)
        return JsonResponse(res.text,safe=False)
        # try:
        #
        #
        #     return JsonResponse(res.text)
        # except:
        #     response = JsonResponse({'status': '颜龄检测服务器未工作'})
        #     response.status_code = 400
        #     return response

def faceagingcaae(request):
    STYLETRANSFER_SERVER_URL = 'http://127.0.0.1:8004/show/'
    PIC_FOLDER = './faceaging/py_scripts/faceagingcaae/'
    if request.method == "POST":
        if 'pic' in request.POST:
            print("收到PIC")
            PIC_ID = request.POST.get('pic', '')
            nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")
            serverUrl = PIC_ID+"_"+nickname+"_"+str(request.FILES['faceagingcaae'])
            THIS_FILE_PATH = PIC_FOLDER + serverUrl
            with open(THIS_FILE_PATH, 'wb+') as destination:
                for chunk in request.FILES['faceagingcaae'].chunks():
                    destination.write(chunk)
            return JsonResponse({'serverUrl':serverUrl})
    if 'image1path' in request.POST:  # 说明是开始处理的的请求

        image1path = request.POST.get('image1path', '')
        nickname = request.POST.get('nickname', '').encode("gbk", "ignore").decode("gbk")

        files = {
            "image": (image1path, open(PIC_FOLDER + image1path, 'rb'), 'image/png', {}),
        }
        res = requests.post(STYLETRANSFER_SERVER_URL, data={"id": nickname}, files=files)
        # print(res.text)
        return JsonResponse(res.text,safe=False)
        # try:
        #
        #
        #     return JsonResponse(res.text)
        # except:
        #     response = JsonResponse({'status': '颜龄检测服务器未工作'})
        #     response.status_code = 400
        #     return response

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
        if Album.objects.filter(nickname=nickname,albumname=albumname):
            print("相册重复创建")
            response =  JsonResponse({'status': '相册重复创建'})
            response.status_code = 400
            return response
        newAlbum = Album(nickname=nickname,albumname=albumname,visibility=visibility,totalsum=0)
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
            current_color = ['#FF9900','#0099CC','#FF6666','#CCCCCC','#009933','#009999','#99CC00','#FF9900','#33CC99','#006699']
            array_return.append({
                "albumname":item.albumname,
                "visibility": item.visibility,
                "createtime": str(item.createtime)[:10],
                "backgroundcolor":current_color[random.randint(0,len(current_color)-1)],
                "totalsum": item.totalsum
            })
        return JsonResponse(array_return,safe=False)
    if request.method == "DELETE":
        print("删除相册请求")
        delete_content = QueryDict(request.body)
        nickname = delete_content.get('nickname', '').encode()
        albumname = delete_content.get('albumname', '')
        obje = Album.objects.get(nickname=nickname,albumname=albumname)
        obje.delete()
        for item in AlbumDetail.objects.filter(nickname=nickname, albumname=albumname):
            item.delete()
        return JsonResponse({'status': 'success'})

@authentication_classes([])
def albumdetail(request):
    if request.method == 'GET':
        nickname = request.GET.get('nickname', '').encode()
        albumname = request.GET.get('albumname', '')

        array_return = []   #要返回的数组
        current_time = ""   #一条记录中的时间信息
        current_saying = "" #一条记录中的文字信息
        url_list = []       #一条记录中的图片URL集合
        item_counter=0
        for i, item in enumerate(AlbumDetail.objects.filter(nickname=nickname,albumname=albumname)):
            if i==0:
                current_time = item.createtime
                djangocreatetime = item.djangocreatetime
                current_saying = item.upload_content
                url_list=[item.pic_data.url]
                item_counter = 1
            else:
                if item.createtime == current_time:
                    url_list.append(item.pic_data.url)
                    item_counter +=1
                else:
                    array_return.append({
                        "createtimeMonth": str(djangocreatetime)[5:7],
                        "createtimeDay": str(djangocreatetime)[8:10],
                        "createtimeTime": str(djangocreatetime)[11:19],
                        "createtime": current_time,
                        "upload_content": current_saying,
                        "url_list": list(url_list),
                        "item_counter":item_counter
                    })
                    current_time = item.createtime
                    current_saying = item.upload_content
                    url_list=[item.pic_data.url]
                    item_counter = 1
        array_return.append({
            "createtimeMonth": str(djangocreatetime)[5:7],
            "createtimeDay": str(djangocreatetime)[8:10],
            "createtimeTime": str(djangocreatetime)[11:19],
            "createtime":current_time,
            "upload_content": current_saying,
            "url_list": list(url_list),
            "item_counter": item_counter
        })
        print(array_return)
        return JsonResponse(array_return, safe=False)
    if request.method == 'POST':  # 添加照片请求
        print("request POST:", str(request.POST).encode("gbk", "ignore").decode("gbk"))
        # print("request FILE:", request.FILES)  # official page 1301
        # print("request FILE DETAIL:", request.FILES['albumdetail'])  # 传递过来的name参数中是什么就用什么来访问，这里测试的是file-name
        pic_data = request.FILES['albumdetail']
        nickname = request.POST.get('nickname', '').encode()
        albumname = request.POST.get('albumname', '')
        upload_content = request.POST.get('upload_content', '')
        createtime = request.POST.get('createtime', '')
        createtime = createtime[1:len(createtime)-1]    #处理小程序JSON.stringify来的一对引号
        print(createtime)
        newAlbumDetail = AlbumDetail(nickname=nickname,albumname=albumname,createtime=createtime,pic_data=pic_data,upload_content=upload_content)
        newAlbumDetail.save()
        # 相册图片数目+1
        thisAlbum = Album.objects.get(nickname=nickname,albumname=albumname)
        thisAlbum.totalsum += 1
        thisAlbum.save()
        print("上传图片请求响应完成：albumdetail——POST")
        return JsonResponse({"status": True})
    if request.method == 'DELETE':
        print("删除记录请求")
        delete_content = QueryDict(request.body)
        nickname = delete_content.get('nickname', '').encode()
        albumname = delete_content.get('albumname', '')
        createtime = delete_content.get('createtime', '')

        item = AlbumDetail.objects.filter(nickname=nickname,albumname=albumname,createtime=createtime)
        _t = Album.objects.get(nickname=nickname, albumname=albumname)
        _t.totalsum = _t.totalsum - len(item)
        _t.save()

        AlbumDetail.objects.filter(nickname=nickname, albumname=albumname, createtime=createtime).delete()
        return JsonResponse({'status': 'success'})



