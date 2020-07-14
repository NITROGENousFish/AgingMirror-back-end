
# PROJECT FINISHED!!! おめでとうございます!!!

**项目结题验收评分89.70** ，前后端全栈，希望能够评一个国家级项目

# July 2020
提交内容分为**算法服务器**和**微信小程序服务器**

**微信小程序服务器**中已经删除了如下的一些能力SecreteKey，请自行添加

    微信小程序 APPID，APPSECRET（用于申请小程序用户openid）
    位置:\AgingMirror-back-end\wechat\faceaging\openid.py

    Tencent Cloud API   腾讯云基础信息 App_ID，App_Key
    位置:\AgingMirror-back-end\wechat\faceaging\py_scripts\tencent_faceaging.py

**算法服务器**  模型已经删除，一共有四个算法服务器。~~但是由于在提交结题验收之后整理代码电脑崩溃，实际上只存活下来两个半~~

算法服务器采用virtualenvwrapper-win将每一个算法封装为一个django服务，让微信小程序与其进行交互。

![image](https://github.com/NITROGENousFish/AgingMirror-back-end/raw/master/structure.png)

算法服务器虚拟环境指南(基本涵盖了如下内容)

    tensorflow 1.X
    tensorflow 2.X
    pytorch
    dlib
    openCV
    scikit-image
# June 2020

项目的第二个后端版本
相册功能已经完全上线，并且修正了登录授权的判定

    mysql 8.0 as databases
      databases settings(settings.py):
      'NAME': 'faceaging_django', # 数据库名
      'USER': 'faceaging', # 账号
      'PASSWORD': 'faceaging', # 密码



**pip list in server: 服务器的piplist如下：**

    certifi                 2020.4.5.1
    chardet                 3.0.4
    Django                  2.1.4
    django-redis            4.11.0
    djangorestframework     3.11.0
    djangorestframework-jwt 1.11.0
    idna                    2.9
    pip                     20.1.1
    Pygments                2.6.1
    PyJWT                   1.7.1
    PyMySQL                 0.9.3
    pytz                    2020.1
    redis                   3.5.2
    requests                2.23.0
    selenium                3.141.0
    setuptools              45.3.0
    urllib3                 1.25.9
    wheel                   0.34.2

# May 2020
项目的第一个迭代，详情内容请见六月份迭代。