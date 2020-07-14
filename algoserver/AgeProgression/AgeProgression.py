import model
import consts
import logging
import os
import re
import numpy as np
import argparse
import sys
import random
import datetime
import torch
from utils import *
from torchvision.datasets.folder import pil_loader
import gc
import torch
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

gc.collect()

assert sys.version_info >= (3, 6),\
    "This script requires Python >= 3.6"  # TODO 3.7?
assert tuple(int(ver_num) for ver_num in torch.__version__.split('.')) >= (0, 4, 0),\
    "This script requires PyTorch >= 0.4.0"  # TODO 0.4.1?

def agePro(input,output,gender):
    mode = 'test'
    # train params
    epochs = 300
    choices = 'always'
    batch_size = 16
    weight_decay = 1e-5
    learning_rate = 8e-4
    b1 = 0.5
    b2 = 0.999
    shouldplot = False

    # test params
    age = 0
    gender = gender
    watermark = False

    # shared params
    cpu = False
    load = './AsianFourResult/epoch11'
    z_channels = 50

    consts.NUM_Z_CHANNELS = z_channels
    net = model.Net()

    if cpu==True and torch.cuda.is_available():
        net.cuda()


    if load is None:
        raise RuntimeError("Must provide path of trained models")

    net.load(path=load, slim=True)


    image_tensor = pil_to_model_tensor_transform(pil_loader(input)).to(net.device)
    net.test_single(
        image_tensor=image_tensor,
        age=20,
        gender=gender,
        target=output,
        watermark=None
    )
    return './output/'+'menifa.png'





# =================================================================================================================
from flask import request, Flask, jsonify
import base64
import logging, sys, os
import traceback
logging.basicConfig(stream=sys.stderr)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/show', methods=['POST'])
def post_Data():
    try:  
        idd = request.form['id']
        image = request.files['file']
        image_path = "./input/"+idd+".jpg"
        image.save(image_path)
        result_url_male = './output/'+idd+'_male.jpg'
        result_url_female = './output/'+idd+'_female.jpg'
        print('Hello world!', file=sys.stderr)
        agePro(image_path,result_url_male,0)
        agePro(image_path,result_url_female,1)
        img_base64_data_male = base64.b64encode(open(result_url_male, 'rb') .read()).decode()
        img_base64_data_female = base64.b64encode(open(result_url_female, 'rb') .read()).decode()
        res={
            "pic_male":'data:image/png;base64,'+img_base64_data_male,
            "pic_female":'data:image/png;base64,'+img_base64_data_female,
        }
        return jsonify(res)
    except Exception:  
        traceback.print_exc() 
    


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8004)
    # agePro('./input/after.jpg','./output/after_male.jpg',0)
    # agePro('./input/after.jpg','./output/after_female.jpg',1)