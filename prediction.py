import numpy as np
import cv2
import os
import dlib
import time
from imutils import face_utils
from os import listdir

face_rec = cv2.CascadeClassifier('model_image/haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('model_image/shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('model_image/dlib_face_recognition_resnet_model_v1.dat')


def imshow_RGB():
    kernel = np.ones((5, 5), np.uint8)  # bit 8
    img = cv2.imread('static/images/41019220.jpg')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gray_img, (9, 9), 0)
    threshold = cv2.Canny(img, 100, 100)
    dialation = cv2.dilate(threshold, kernel=kernel, iterations=1)
    ercoded = cv2.erode(dialation, kernel=kernel, iterations=1)

    cv2.imshow('Original', img)
    cv2.imshow('Gray', gray_img)
    cv2.imshow('Blur', blur_img)
    cv2.imshow('Threshold', threshold)
    cv2.imshow('Dialaation', dialation)
    cv2.imshow('ercoded', ercoded)
    cv2.waitKey(0)


def face_img(file_img):
    face_rec = cv2.CascadeClassifier('model_image/haarcascade_frontalface_default.xml')
    scale = 0.5
    img = cv2.imread(file_img)
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bBoxes = face_rec.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))  # model ML
    len_img = len(bBoxes)
    print(bBoxes)
    print(f'found face: {len_img}')
    for (x, y, w, h) in bBoxes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        cv2.putText(img, 'Hello World', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 3, cv2.LINE_AA)
    cv2.imwrite('face_rec.png', img)
    cv2.imshow('img', img)
    cv2.waitKey(0)


def face_video():
    cap = cv2.VideoCapture('model_image/mindset.mp4')
    while True:
        ret, image = cap.read()
        scale = 0.5
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        bBoxes = face_rec.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in bBoxes:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, 'Hello Python', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 3,
                        lineType=cv2.LINE_AA)
        cv2.imshow('img', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def threshold():
    cap = cv2.VideoCapture('model_image/mindset.mp4')
    while True:
        ret, image = cap.read()
        scale = 0.5
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        res, threshold = cv2.threshold(gray_scale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        bBoxes = face_rec.detectMultiScale(gray_scale, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        print(bBoxes)
        for x, y, w, h in bBoxes:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3, lineType=cv2.LINE_AA)
            cv2.imwrite('test.jpg', image)
            cv2.imshow('face_detection', image)
            cv2.imshow('threshold', threshold)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def dlib_image(file_image):
    image = cv2.imread(file_image)
    scale = 0.5
    image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dets = detector(gray_scale, 1)
    print(dets)
    for i, rect in enumerate(dets):
        x, y = rect.left(), rect.top()
        w, h = rect.right(), rect.bottom()
        shape = sp(image, rect)  # deep learning
        shape = face_utils.shape_to_np(shape)
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 3)
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 0, 255), -1)

    cv2.imshow('image', image)
    cv2.waitKey(0)


def dlib_video(select):
    cap = cv2.VideoCapture(select)
    while True:
        ret, image = cap.read()
        scale = 0.5
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dets = detector(gray_scale, 1)
        for i, rect in enumerate(dets):
            x, y = rect.left(), rect.top()
            w, h = rect.right(), rect.bottom()
            shape = sp(image, rect)  # deep learning
            shape = face_utils.shape_to_np(shape)
            cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 3)
            write_image = image[y:h, x:w]
            cv2.imwrite('face_dets.png', write_image)
            for (x, y) in shape:
                cv2.circle(image, (x, y), 2, (0, 0, 255), -1)
        cv2.imshow('image', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



