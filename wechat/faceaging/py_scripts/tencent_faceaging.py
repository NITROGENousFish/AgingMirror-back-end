import requests
import os
import base64
import math
import time
from PIL import Image,ImageDraw
import json
import hashlib

#腾讯云基础信息
App_ID  = 1111111111    #腾讯云 int
App_Key = ''

#图像转base64，如果超过API 1M上限则压缩
def read_pic_to_base64(pic_path):
    fsize = os.path.getsize(pic_path)
    if fsize>1024*1024:
        #压缩比例：
        compresed_rate = math.floor(math.sqrt(fsize/float(1024*1024)))
        sImg=Image.open(pic_path)
        w,h=sImg.size
        dImg=sImg.resize((int(w/compresed_rate),int(h/compresed_rate)),Image.ANTIALIAS)  #设置压缩尺寸和选项，注意尺寸要用括号
        dImg.save(pic_path)
        #压缩图片
    with open(pic_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        #s = base64_data.decode()
    return base64_data


def processFaceagingPicture(pic_1_file_path,pic_2_file_path):
    pic1base64 = read_pic_to_base64(pic_1_file_path)
    pic2base64 = read_pic_to_base64(pic_2_file_path)

    post_params = {
        "app_id":App_ID,
        "time_stamp":int(time.time()),
        "nonce_str":hashlib.md5(str(int(time.time())).encode(encoding='UTF-8')).hexdigest(),
        # "sign":"",        
        "source_image":pic1base64,
        "target_image":pic2base64
    }
    
    

    ###接口鉴权   https://ai.qq.com/doc/auth.shtml
    # 将<key, value>请求参数对按key进行字典升序排序，得到有序的参数对列表N
    from urllib.parse import urlencode
    result_list = []
    for i in sorted (post_params) : 
        # print ((i, post_params[i]), end =" ") 
        post_params_in ={i:post_params[i]}
        result_list.append(urlencode(post_params_in))
        result = "&".join(result_list)
    # print(result)
    # 将列表N中的参数对按URL键值对的格式拼接成字符串，得到字符串T（如：key1=value1&key2=value2），URL键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8，而不是小写%e8
    sort_dict = sorted(post_params.items(), key=lambda item: item[0], reverse=False)  # 排序操作
    sort_dict.append(('app_key','MIyTYQkJYo0a5eqG'))
    result = urlencode(sort_dict)
    # 将应用密钥以app_key为键名，组成URL键值拼接到字符串T末尾，得到字符串S（如：key1=value1&key2=value2&app_key=密钥)
   # result += "&app_key=" + App_Key
    # 对字符串S进行MD5运算，将得到的MD5值所有字符转换成大写，得到接口请求签名
    
    out = hashlib.md5(result.encode(encoding='UTF-8')).hexdigest()
    out = str(out).upper()
    ###接口鉴权结束
    
    post_params['sign'] = out

    #发起API请求
    headers={
        "Content-Type":"application/x-www-form-urlencoded",
    }

    re = requests.post("https://api.ai.qq.com/fcgi-bin/face/face_detectcrossageface",data = post_params,headers=headers).json()

    data = re['data']
    source_face = data['source_face']
    x1_s = source_face['x1']
    x2_s = source_face['x2']
    y1_s = source_face['y1']
    y2_s = source_face['y2']
    target_face = data['target_face']
    x1_t = target_face['x1']
    x2_t = target_face['x2']
    y1_t = target_face['y1']
    y2_t = target_face['y2']

    im1 = Image.open(pic_1_file_path)
    draw1 = ImageDraw.Draw(im1)
    draw1.line([(x1_s, y1_s), (x1_s, y2_s), (x2_s, y2_s), (x2_s, y1_s), (x1_s, y1_s)], width=4, fill='red')
    im1.save(pic_1_file_path)

    im2 = Image.open(pic_2_file_path)
    draw2 = ImageDraw.Draw(im2)
    draw2.line([(x1_t, y1_t), (x1_t, y2_t), (x2_t, y2_t), (x2_t, y1_t), (x1_t, y1_t)], width=4, fill='red')
    im2.save(pic_2_file_path)

    return re['data']['score']
if __name__ == "__main__":
    processFaceagingPicture('./1.jpg','./2.jpg')
