import os
import io
from google.cloud import vision
import numpy as np
from PIL import Image
import pytesseract
import cv2


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

    def document_google(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.image, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        x_axis = []
        y_axis = []
        txt = ''
        for text in texts:
            txt += text.description
            for vertex in text.bounding_poly.vertices:
                x_axis.append(vertex.x)
                y_axis.append(vertex.y)
        return txt, x_axis, y_axis

    def document_tesseract(self):
        text_classifier = pytesseract.image_to_string(Image.open(self.image), lang='tha')
        image = cv2.imread(self.image)
        scale = 0.5
        img_convert = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        cv2.imshow('img', img_convert)
        cv2.waitKey(3)
        return text_classifier
