import cv2
import time
import os
from os import listdir
import numpy
import dlib

img_pixel = 128
input_path = 'datasets/images/'
output_path = 'datasets/images_crops/'
input_files = listdir('./' + input_path)

face_rec = cv2.CascadeClassifier('model_image/haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('model_image/shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('model_image/dlib_face_recognition_resnet_model_v1.dat')

avg = []
_strtime = time.time()
for i, name in enumerate(input_files):
    color_img = cv2.imread(input_path + name)
    gray_scale = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    dets = detector(gray_scale, 1)
    for k, rect in enumerate(dets):
        x, y = rect.left(), rect.top()
        w, h = rect.right(), rect.bottom()
        write_img_color = color_img[y:h, x:w]
        image = cv2.resize(write_img_color, (img_pixel, img_pixel), interpolation=cv2.INTER_AREA)
        cv2.imwrite(output_path + name, image)
        sec = (time.time() - _strtime)
        avg.append(sec)
        print(output_path + name)
        print('average: ', time.time() - _strtime)
avg = avg[-1] / len(avg)
print('Average : {} sec'.format(str(round(avg, 2))))
