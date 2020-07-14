import os
import base64
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
# Create your views here.
from age_detector.forms import AddForm
from age_detector.core.guess import *

def test(request):
    return render(request, "age_detector/html/show.html")

def detect(request):
    if request.method == "POST":

        # af = AddForm(request.POST, request.FILES)

        id = request.POST.get("id")
        # id_path = af.cleaned_data["id"]+".jpg"
        # 读取内容图片

        image = request.FILES.get("image")
        # print(image)
        # image = af.cleaned_data["image"]
        image_path = os.path.join('static/age_detector/input/', id + ".jpg")
        image_file = open(image_path, 'wb+')
        for chunk in image.chunks(chunk_size=1024):
            image_file.write(chunk)
        
        dic = start(image_path, id)
        print("____________________________")
        print(dic)
        print("____________________________")
        out_array = []
        for key in dic:
            img_base64_data = base64.b64encode(open('static/age_detector/output/'+key, 'rb') .read()).decode()
            out_array.append(['data:image/png;base64,'+img_base64_data,list(map(str,dic[key]))])
        img_head_base64_data = base64.b64encode(open(os.path.join('static/age_detector/output/', id + ".jpg"), 'rb') .read()).decode()
        res={
            "overall-array":['data:image/png;base64,'+img_head_base64_data,str(len(dic))],
            'content-array':out_array
        }
        # print(res)
        return JsonResponse(res)
        # return render(request, "age_detector/html/show.html", context={
        #     "num": len(dic),
        #     "results": dic
        # })
    else:
        af = AddForm()
        return render(request, 'age_detector/html/add.html', context={"af": af})
