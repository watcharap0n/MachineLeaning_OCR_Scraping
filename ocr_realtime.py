import numpy as np
import cv2
import dlib
from imutils import face_utils
import pickle
import pandas as pd
from PIL import Image
from google.cloud import vision
import io

face_rec = cv2.CascadeClassifier('model_image/haarcascade_frontalface_default.xml')
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('model_image/shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('model_image/dlib_face_recognition_resnet_model_v1.dat')

cap = cv2.VideoCapture(0)
client = vision.ImageAnnotatorClient()

while True:
    ret, image = cap.read()
    cv2.imwrite('instance/ocr_image.jpg', image)
    with io.open('instance/ocr_image.jpg', 'rb') as image_file:
        content = image_file.read()
    feature = vision.Image(content=content)
    response = client.text_detection(image=feature)
    texts = response.text_annotations
    df = pd.DataFrame(columns=['locale', 'description', 'vertextX', 'vertextY'])
    for text in texts:
        vertices = ([(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description,
                vertextX=vertices[0],  # left top
                vertextY=vertices[2],  # right bottom
                vertextX1=vertices[1],  # right top
                vertextY1=vertices[3]  # left bottom
            ),
            ignore_index=True
        )
    dict_image = df.to_dict()
    idx_image = len(dict_image['vertextX'])
    for i in range(idx_image)[1:]:
        x, y = dict_image['vertextX'][i]
        w, h = dict_image['vertextY'][i]
        x1, y1 = dict_image['vertextX1'][i]
        w1, h1 = dict_image['vertextY1'][i]
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 1)
    cv2.imshow('ocr_video', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
