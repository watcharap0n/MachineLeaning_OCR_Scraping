import pickle
import time
import cv2
import dlib
import os

path = 'datasets/labels/'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('model_image/shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('model_image/dlib_face_recognition_resnet_model_v1.dat')

FACE_DETS = []
FACE_NAME = []
time_avg = []
stff = time.time()
for fn in os.listdir(path):
    for idx, i in enumerate(os.listdir(path + fn)):
        if i.endswith('.jpg') or i.endswith('.png') or i.endswith('.jpeg'):
            img = cv2.imread(path + os.path.sep + fn + os.path.sep + i, cv2.COLOR_BGR2RGB)
            dets = detector(img, 1)
            for k, d in enumerate(dets):
                shape = sp(img, d)
                face_desc = model.compute_face_descriptor(img, shape, 1)
                FACE_DETS.append(face_desc)
                FACE_NAME.append(fn)
                idx += 1
                sec = (time.time() - stff)
                time_avg.append(sec)
                print('Done... {} {:.2f} '.format(path + fn, sec))
avg = time_avg[-1] / len(time_avg)
print('avg: {} sec '.format(str(round(avg, 2))))
pickle.dump((FACE_DETS, FACE_NAME), open('train_datasets.pk', 'wb'))
