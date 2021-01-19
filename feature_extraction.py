import pickle
import time
import cv2
import dlib
import os
from PIL import Image

path = 'datasets/images_labels/'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('model_image/shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('model_image/dlib_face_recognition_resnet_model_v1.dat')

FACE_DECS = []
FACE_NAME = []
current_id = 0
LABEL_IDX = {}

count = 1
stff = time.time()
for fn in os.listdir(path):
    for i in os.listdir(path + fn):
        if i.endswith('.jpg') or i.endswith('.png') or i.endswith('.jpeg'):
            img = cv2.imread(path + os.path.sep + fn + os.path.sep + i, cv2.COLOR_BGR2RGB)
            dets = detector(img, 1)
            for k, d in enumerate(dets):
                shape = sp(img, d)
                face_desc = model.compute_face_descriptor(img, shape, 1)
                FACE_DECS.append(face_desc)
                FACE_NAME.append(fn)
                print('Done {} {} in {:.2f} sec'.format(count, fn + '/' + i, (time.time() - stff)))
                count += 1
pickle.dump((FACE_DECS, FACE_NAME), open('train_datasets.pk', 'wb'))

