from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import math
import time
from age_detector.core.data import inputs
import numpy as np
import tensorflow as tf
from age_detector.core.model import select_model, get_checkpoint
from age_detector.core.utils import *
import os
import json
import csv

RESIZE_FINAL = 227
GENDER_LIST = ['M', 'F']
AGE_LIST = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
MAX_BATCH_SZ = 128



def resolve_file(fname):
    if os.path.exists(fname): return fname
    for suffix in ('.jpg', '.png', '.JPG', '.PNG', '.jpeg'):
        cand = fname + suffix
        if os.path.exists(cand):
            return cand
    return None


def classify_one_multi_crop(sess, label_list, softmax_output, coder, images, image_file, writer):
    try:

        print('Running file %s' % image_file)
        image_batch = make_multi_crop_batch(image_file, coder)

        batch_results = sess.run(softmax_output, feed_dict={images: image_batch.eval()})
        output = batch_results[0]
        batch_sz = batch_results.shape[0]

        for i in range(1, batch_sz):
            output = output + batch_results[i]

        output /= batch_sz
        best = np.argmax(output)
        best_choice = (label_list[best], output[best])
        print('Guess @ 1 %s, prob = %.2f' % best_choice)

        nlabels = len(label_list)
        second_best = None
        if nlabels > 2:
            output[best] = 0
            second_best = np.argmax(output)
            print('Guess @ 2 %s, prob = %.2f' % (label_list[second_best], output[second_best]))

        if writer is not None:
            writer.writerow((image_file, best_choice[0], '%.2f' % best_choice[1]))
        return best_choice, (label_list[second_best], output[second_best])
    except Exception as e:
        print(e)
        print('Failed to run image %s ' % image_file)
        return None


def list_images(srcfile):
    with open(srcfile, 'r') as csvfile:
        delim = ',' if srcfile.endswith('.csv') else '\t'
        reader = csv.reader(csvfile, delimiter=delim)
        if srcfile.endswith('.csv') or srcfile.endswith('.tsv'):
            print('skipping header')
            _ = next(reader)

        return [row[0] for row in reader]


def start(input_path, id):
    device_id = '/gpu:0'
    model_dir = 'age_detector/core/22801'
    tf.reset_default_graph()

    files = []

    face_detections = face_detect(id)
    face_files, rectangles = face_detections.run(input_path)
    print(face_files)
    files += face_files

    config = tf.ConfigProto(allow_soft_placement=True)
    with tf.Session(config=config) as sess:

        label_list = AGE_LIST
        nlabels = len(label_list)

        print('Executing on %s' % device_id)
        model_fn = select_model('inception')

        with tf.device(device_id):

            images = tf.placeholder(tf.float32, [None, RESIZE_FINAL, RESIZE_FINAL, 3])
            logits = model_fn(nlabels, images, 1, False)
            init = tf.global_variables_initializer()

            checkpoint_path = '%s' % (model_dir)

            model_checkpoint_path, global_step = get_checkpoint(checkpoint_path, None, 'checkpoint')

            saver = tf.train.Saver()
            saver.restore(sess, model_checkpoint_path)

            softmax_output = tf.nn.softmax(logits)

            coder = ImageCoder()

            # Support a batch mode if no face detection model
            if len(files) == 0:
                if (os.path.isdir(input_path)):
                    for relpath in os.listdir(input_path):
                        abspath = os.path.join(input_path, relpath)

                        if os.path.isfile(abspath) and any(
                                [abspath.endswith('.' + ty) for ty in ('jpg', 'png', 'JPG', 'PNG', 'jpeg')]):
                            print(abspath)
                            files.append(abspath)
                else:
                    files.append(input_path)
                    # If it happens to be a list file, read the list and clobber the files
                    if any([input_path.endswith('.' + ty) for ty in ('csv', 'tsv', 'txt')]):
                        files = list_images(input_path)

            writer = None
            output = None
            image_files = list(filter(lambda x: x is not None, [resolve_file(f) for f in files]))

            ageDict = dict()
            for image_file in image_files:
                result = classify_one_multi_crop(sess, label_list, softmax_output, coder, images, image_file, writer)
                # ageDict[os.path.basename(image_file)] = "年龄最可能在"+result[0][0]+"区间内，置信度为"+str(result[0][1])+"，" \
                #                                         "第二可能在"+result[1][0]+"区间内，置信度为"+str(result[1][1]) + "。"
                ageDict[os.path.basename(image_file)] = [result[0][0],result[0][1],result[1][0],result[1][1]]
            if output is not None:
                output.close()


            return ageDict
