import cv2
from vision_machine_optical import VisionOCR
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


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
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.imshow('img', image)
    cv2.waitKey(0)
    return ocr


def add_transition(num=int()):
    num = np.arange(num)
    add_num = int()
    for idx, new_num in enumerate(num):
        add_num += new_num
    return add_num


def transform_image():
    img = cv2.imread('static/images/paper.jpeg')
    width, height = 400, 700
    pts1 = np.float32([[154, 10], [578, 10], [160, 728], [587, 726]])  # left, right, left bottom, right bottom
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_output = cv2.warpPerspective(img, matrix, (width, height))
    cv2.imshow('image', img_output)
    cv2.waitKey(0)


def transform_document_mango():
    ocr = VisionOCR('static/images/paper.jpeg')
    dfs = ocr.document_pandas()
    dict_image = dfs.to_dict()
    idx_image = len(dict_image['vertextX'])
    image = cv2.imread('static/images/paper.jpeg')
    x, y = dict_image['vertextX'][0]
    w, h = dict_image['vertextY'][0]
    x1, y1 = dict_image['vertextX1'][0]
    w1, h1 = dict_image['vertextY1'][0]
    width, height = 400, 700
    pts1 = np.float32([[x - 10, y - 10], [x1 + 10, y1 - 10], [w1 - 10, h1 + 10], [w + 10, h + 10]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transform = cv2.warpPerspective(image, matrix, (width, height))
    for i in range(idx_image)[1:]:
        x, y = dict_image['vertextX'][i]
        w, h = dict_image['vertextY'][i]
        x1, y1 = dict_image['vertextX1'][i]
        w1, h1 = dict_image['vertextY1'][i]
        print((x, y), (w, h), (x1, y1), (w1, h1))
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 3)
    cv2.imshow('origin', image)
    cv2.imshow('image', transform)
    cv2.waitKey(0)


def titanic_imp():
    f = pd.read_csv('instance/titanic_data.csv')
    origin_age = f['Age'].isnull()
    age = f['Age'].values
    age = np.reshape(age, (-1, 1))
    imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')  # แทนค่า NaN เป็น float
    imp.fit(age)
    f['Age'] = imp.transform(age)
    X = f[['Pclass', 'Fare']]
    y = f['Survived']
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    lr = KNeighborsClassifier()
    lr.fit(x_train, y_train)
    y_pred = lr.predict(x_test)
    print(accuracy_score(y_pred, y_test))
