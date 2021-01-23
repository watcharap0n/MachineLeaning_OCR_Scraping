import cv2
from os import listdir
import dlib
import time


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('model_image/shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('model_image/dlib_face_recognition_resnet_model_v1.dat')

img_pixel = 128
input_path = 'datasets/images/'
output_path = 'datasets/cropped/'
input_files = listdir('./' + input_path)

stff = time.time()
for idx, name in enumerate(input_files):
    print('index: {} files name: {}'.format(idx, input_path + name))
    image_color = cv2.imread(input_path + name)
    gray_scale = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
    dets = detector(gray_scale, 1)
    print(dets, name)
    for k, d in enumerate(dets):
        x, y = d.left(), d.top()
        w, h = d.right(), d.bottom()
        cropped_image = image_color[y:h, x:w]  # cropped_image
        image = cv2.resize(cropped_image, (img_pixel, img_pixel), interpolation=cv2.INTER_AREA)
        cv2.imwrite(output_path + name, image)
        sec = time.time() - stff
        print(f'face: {d} sec: {sec}')

