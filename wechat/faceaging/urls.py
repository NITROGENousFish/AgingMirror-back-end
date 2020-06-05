from django.urls import path

from . import views

urlpatterns = [
    path('onLogin', views.onLogin, name='onLogin'), #微信小程序登录接口
    path('album', views.album, name='album'),
    path('albumdetail', views.albumdetail, name='albumdetail'),
    path('findlostpeople', views.findlostpeople, name='findlostpeople'),        #主页寻人接口
]