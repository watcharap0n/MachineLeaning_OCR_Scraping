import os
import io
from collections import OrderedDict
from google.cloud import vision
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import cv2
from matplotlib import pyplot as plt
from matplotlib import patches as pch

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'config/config_ocr.json'


class VisionOCR:
    def __init__(self, image):
        self.image = image

    def vision_environment(self):
        client = vision.ImageAnnotatorClient()
        file_name = os.path.abspath(self.image)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels: ')
        for label in labels:
            print(label.description)

    def document_spilt_text(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as file:
            content = file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        lst = []
        for i in texts:
            text = str(i.description).split()
            lst.append(text)
        print(lst)
        ocr = ''.join(lst[0])
        return ocr

    def document_google(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        txt = ''
        for text in texts:
            txt += text.description
        return txt

    def document_google_plot(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        x_axis = []
        y_axis = []
        txt = ''
        a = plt.imread(self.image)
        fig, ax = plt.subplots(1)
        ax.imshow(a)

        for text in texts:
            txt += text.description
            for vertex in text.bounding_poly.vertices:
                x_axis.append(vertex.x)
                y_axis.append(vertex.y)
            vertices = ([(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])
            X = vertices[0]
            X1 = vertices[1]
            Y = vertices[2]
            rect = pch.Rectangle(X, (X1[0] - X[0]),
                                 (Y[1] - X[1]), linewidth=1,
                                 edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        plt.show()
        return txt

    def document_pandas(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as image_file:
            content = image_file.read()
        feature = vision.Image(content=content)
        response = client.text_detection(image=feature)
        texts = response.text_annotations
        df = pd.DataFrame(columns=['locale', 'description', 'vertextX', 'vertextY'])
        for text in texts:
            vertices = ([(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])
            # print(vertices[0], vertices[2])
            df = df.append(
                dict(
                    locale=text.locale,
                    description=text.description,
                    vertextX=vertices[0],
                    vertextY=vertices[2]
                ),
                ignore_index=True
            )
        return df

    def document_uri(self):
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = self.image
        response = client.text_detection(image=image)
        texts = response.text_annotations

        df = pd.DataFrame(columns=['locale', 'description'])
        for text in texts:
            df = df.append(
                dict(
                    locale=text.locale,
                    description=text.description
                ),
                ignore_index=True
            )
            return df

    def document_tesseract(self):
        text_classifier = pytesseract.image_to_string(Image.open(self.image), lang='tha')
        image = cv2.imread(self.image)
        scale = 0.5
        img_convert = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        img = cv2.threshold(img_convert, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imshow('img', img)
        cv2.waitKey(3)
        return text_classifier


def edu_resize(image):
    img = cv2.imread(image)
    img_resize = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    img_cropped = img[0:200, 200:500]
    cv2.imshow('Original', img)
    cv2.imshow('Resize', img_resize)
    cv2.imshow('Cropped', img_cropped)
    cv2.waitKey(0)


def edu_gray(image):
    img = cv2.imread(image)
    kernel = np.ones((5, 5), np.uint8)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (9, 9), 0)
    img_threshold = cv2.Canny(img, 100, 100)
    img_dialation = cv2.dilate(img_threshold, kernel=kernel, iterations=1)
    img_ercoded = cv2.erode(img_dialation, kernel=kernel, iterations=1)
    cv2.imshow('Gray Image', img_gray)
    cv2.imshow('Blur Image', img_blur)
    cv2.imshow('Threshole', img_threshold)
    cv2.imshow('dialation', img_dialation)
    cv2.imshow('ercoded', img_ercoded)
    cv2.waitKey(0)


def edu_numpy():
    square = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    square[0][1] = 4
    square[1][0:] = np.arange(3)
    a = np.zeros((3, 4), dtype='int')
    b = np.ones((3, 4), dtype='float')
    c = np.identity(3, dtype='int')
    d = np.eye(3, 5)


def dimention_img():
    img = np.zeros((512, 512, 3), np.uint8)  # height, width
    cv2.rectangle(img, (0, 0), (250, 350), (0, 0, 255), 3)  # width height
    cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 255, 0), 3)
    cv2.circle(img, (400, 50), 30, (255, 0, 0), 3)
    cv2.imshow('images', img)
    cv2.waitKey(0)


def rectangle_document(path):
    path = path
    ocr = VisionOCR(path)
    ocr = ocr.document_pandas()
    ocr = ocr.to_dict()
    vert = len(ocr['vertextX'])
    image = cv2.imread(path)
    for i in range(0, vert):
        left, top = ocr['vertextX'][i]
        right, bottom = ocr['vertextY'][i]
        # description = ocr['description'][i]
        # cv2.putText(images, description, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 1)
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.imshow('img', image)
    cv2.waitKey(0)
    return ocr

    # left, top = ocr['vertextX'][0]
    # right, bottom = ocr['vertextY'][0]
    # width, height = 250, 350
    # print(ocr['vertextX'][0], ocr['vertextY'][0])
    # pts1 = np.float32([[top, left], [bottom, height], [right, width], [bottom, right]])
    # pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # imgOutput = cv2.warpPerspective(image, matrix, (width, height))
    # cv2.imshow('output', imgOutput)




# ocr = VisionOCR('static/images/test.png')
# ocr = ocr.document_pandas()
# ocr = ocr.to_dict()
# texts = ocr['description']
# xy = ocr['vertextX']
# wh = ocr['vertextY']
# range_text = len(texts)
#
# embedding = []
# for i in range(range_text)[1:]:
#     x, y = xy[i]
#     embedding.append(y)
#
# cut_y = list(OrderedDict.fromkeys(embedding).keys())
# results = []
# count = 1
# for i in range(range_text)[1:]:
#     x, y = xy[i]
#     w, h = wh[i]
#     text = texts[i]
#     for e, idx in enumerate(cut_y):
#         if idx == y:
#             dic = {e: text}
#             results.append(dic)
#
# len_results = len(results)
# vals = []
# for i in results:
#     if i:
#         vals.append(i)
#
#
# merged = {}
# for k, d in enumerate(vals):
#     for j, v in d.items():
#         if j not in merged:
#             merged[j] = []
#         merged[j].append(v)
#
# merged['company'] = merged.pop(0)
# merged['tax_id'] = merged.pop(10)
# merged['pos_id'] = merged.pop(13)
# merged['date'] = merged.pop(15)
# merged['list_1'] = merged.pop(21)
# merged['list_2'] = merged.pop(23)
# merged['total_each'] = merged.pop(29)
# merged['pro_1'] = merged.pop(30)
# merged['pro_2'] = merged.pop(31)
# merged['pro_3'] = merged.pop(32)
# merged['price_1'] = merged.pop(33)
# merged['price_2'] = merged.pop(34)
# merged['credit'] = merged.pop(35)
# merged['credit_price'] = merged.pop(36)
#
# print(merged)
# print(texts[0])