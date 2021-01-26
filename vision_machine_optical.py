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
    def __init__(self, image_file):
        self.image = image_file

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

