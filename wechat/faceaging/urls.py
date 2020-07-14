from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('onLogin', views.onLogin, name='onLogin'), #微信小程序登录接口
    path('album', views.album, name='album'),
    path('albumdetail', views.albumdetail, name='albumdetail'),
    path('findlostpeople', views.findlostpeople, name='findlostpeople'),        #主页寻人接口
    path('crossagecomparation', views.crossagecomparation, name='crossagecomparation'),        #跨年龄人脸识别接口
    path('styletransfer', views.styletransfer, name='styletransfer'),        #风格迁移接口
    path('agedetection', views.agedetection, name='agedetection'),        #年龄预测接口
    path('wrinkleadd', views.wrinkleadd, name='wrinkleadd'),        #皱纹添加接口
    path('faceagingcaae', views.faceagingcaae, name='faceagingcaae'),        #人脸老化接口
    # path('media',)
]