import cv2
import os
from glob import glob
from PIL import Image
import numpy as np
import dlib
import math

sourcePath="E:\\BaiduNetdiskDownload\\All-Age-Faces Dataset\\aglined faces"
savepath="E:\\AFdata"
savpath="E:\\cutData"
sapath = "E:\\aliFace"
testdir="C:\\Users\\Administrator\\Downloads\\Face-Aging-CAAE-master\\Face-Aging-CAAE-master\\testdir"
tesdir="E:\\testdir"
facedir="E:\\faces\\female"

predictor_path = 'E:\\shape_predictor_81_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()                 #  使用dlib自带的frontal_face_detector作为我们的人脸提取器
predictor = dlib.shape_predictor(predictor_path)             #  使用官方提供的模型构建特征提取器

def rotate_about_center(src, angle, scale):#src表示图片，angle表示角度，scale表示放缩比例
    w = src.shape[1]#得到宽
    h = src.shape[0]#得到高
    rangle = np.deg2rad(angle)#夹角处理为弧度
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale#新图片的宽高
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)#得到旋转矩阵
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))#中心点的转移
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    return cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)#旋转处理

def get_angle(frame):
    p = get_landmarks(frame)

    if p is not None:
        left_y=0
        right_y=0
        left_x=0
        right_x=0
        for i in range(36,42):
            left_y+=p[i,1]
            right_y+=p[6+i,1]
            left_x+=p[i,0]
            right_x+=p[6+i,0]
        left_x=left_x/6.0
        right_x = right_x/6.0
        left_y=left_y/6.0
        right_y=right_y/6.0
        angle = math.atan((right_y - left_y) / (right_x - left_x)) * 180 / math.pi
    #
    # faces = face_cascade.detectMultiScale(frame)#检测人脸
    # angle = 0 #默认为0，表示不旋转
    # for (x, y, w, h) in faces:
    #     roi_gray = frame[y:y + h, x:x + w]#人脸图
    #     eyes = eye_cascade.detectMultiScale(roi_gray)#得到人眼坐标
    #     x_eye = []
    #     y_eye = []
    #     for (ex, ey, ew, eh) in eyes:
    #         x_eye.append((ex + ew) / 2)
    #         y_eye.append((ey + eh) / 2)
    #     if len(x_eye) == 2:
    #         angle = math.atan((y_eye[1] - y_eye[0]) / (x_eye[1] - x_eye[0])) * 180 / math.pi#计算夹角
    #         break#单张人脸检测
        return angle
    return 0

# def get_face(frame):#截取人脸
#     face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
#     faces = face_cascade.detectMultiScale(frame)
#     if len(faces) > 0:
#         imgROI = frame[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]]  # 前者为高度，后者为宽度
#         imgROI = cv2.resize(imgROI, (256, 256), cv2.INTER_LINEAR)  # 固定大小
#     return imgROI

# frame = cv2.imread("1.jpg")
# cv2.imshow("original",frame)
# cv2.imshow("rotate",rotate_about_center(frame,get_angle(frame),1))
# cv2.waitKey()


def get_landmarks(im):
    # temp_img = im
    # gray = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
    #
    # # 获取人脸分类器
    # dets = detector(gray, 0)  # 返回值是<class 'dlib.dlib.rectangle'>，就是一个矩形

    # for k, d in enumerate(dets):  # enumerate函数的返回值是迭代对象的索引和对应值
    #     temp_img = cv2.rectangle(temp_img, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 1)
    #     shape = predictor(temp_img, d)  # 获取人脸检测器
    #     for num in range(shape.num_parts):
    #         temp_img=cv2.circle(temp_img, (shape.parts()[num].x, shape.parts()[num].y), 2, (0, 255, 0), 1)
    #         temp_img=cv2.putText(temp_img, str(num), (shape.parts()[num].x - 5, shape.parts()[num].y - 5),
    #                     cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 0, 0), 1)
    #     cv2.imshow('temp',temp_img)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    print(names)
    rects = detector(im, 1)
    if (len(rects) != 0):
        return np.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])
    else:
        return None

#
# i=0
# with open('E:\\AFAD-Full\\AFAD-Full\\AFAD-Full.txt',"r") as f:    #设置文件对象
#     strs = f.readline()    #可以是随便对文1件的操作
#     strs=strs[:-1]
#     while(strs!="./20/111/Thumbs.db"):
#         strs=f.readline()
#         strs=strs[:-1]
#     while(strs):
#         print(strs)
#         if strs.split(".")[-1]=='db':
#             strs = f.readline()  # 可以是随便对文1件的操作
#             strs = strs[:-1]
#             continue
#         path = os.path.join(sourcePath,strs)
#         print(path)
#         img = cv2.imread(path)
#         label = int(strs.split("/")[1])
#         gender = 0 if int(strs.split("/")[2])==111 else 1
#         print (label,gender)
#
#         dir=str(label)+'.'+str(gender)
#         file=strs.split("/")[-1]
#         filepath=os.path.join(savepath,dir,file)
#         print (filepath)
#         i=i+1
#         print (i)
#         cv2.imwrite(filepath, img)
#         strs = f.readline()  # 可以是随便对文1件的操作
#         strs = strs[:-1]
#
# file_names = glob(os.path.join(savepath,'9.*','*.jpg'))
file_names = glob(os.path.join(tesdir,'*.*'))
#
# for i in range(10):
#     os.mkdir(sapath+'/'+str(i)+'.0')
#     os.mkdir(sapath + '/' + str(i) + '.1')
#
for file_name in file_names:
    # label = int(file_name.split('\\')[-2].split('.')[0])
    names = str(file_name.split('\\')[-1])

    # num = int(file_name.split('\\')[-2].split('.')[1])
    # if (num<=7380):
    #     s = str(label)+'.1'
    #     path = os.path.join(savepath,s)
    # else:
    #     s = str(label)+'.0'
    #     path = os.path.join(savepath,s)
    #
    # pic = Image.open(file_name)
    # pic = np.array(pic)

    # 旋转人脸图片代码
    pic = cv2.imread(file_name)
    pic = cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
    # face = rotate_about_center(pic,get_angle(pic),1)

    # 裁切人脸图片代码
    p = get_landmarks(pic)

    if p is None:
        continue

    lu_x=min([p[0,0],p[1,0],p[77,0]])
    lu_x=max(lu_x, 0)
    lu_y=min([p[78,1],p[79,1]])
    lu_y=max(lu_y, 0)
    rd_x=max([p[15,0],p[16,0],p[78,0]])
    rd_y=max([p[7,1],p[8,1],p[9,1]])
    face = pic[lu_y:rd_y, lu_x:rd_x, :]


    # 识别人脸并裁切代码（太粗糙）
#     # pic = cv2.imread(file_name)
#     # pic =cv2.cvtColor(pic,cv2.COLOR_BGR2RGB)
#     h = pic.shape[0]
#     w = pic.shape[1]
#     rects = detector(pic, 0)
#     for rect in rects:
#         x1 = rect.left()
#         y1 = rect.top()
#         x2 = rect.right()
#         y2 = rect.bottom()
#         x1 = x1 - 20 if (x1 >= 20) else 0
#         y1 = y1 - 10 if (y1 >= 10) else 0
#         x2 = x2 + 20 if (x2 <= w-20) else w
#         y2 = y2 + 20 if (y2 <= h-20) else h
#

    img = Image.fromarray(face)
    img.save(str(tesdir)+'/'+names)
#    print(str(num)+'.'+str(label)+str(names))
