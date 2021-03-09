import pandas as pd
import json
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, scale, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier



data = pd.read_csv('datasets/data.csv')

x = data[['']]
y = data[['class']]


lst = []
one_q = [q[0] for q in question]
invert = le.inverse_transform(one_q)
print(invert)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.4)
model = KNeighborsClassifier()
model = model.fit(x_train, y_train)
prediction = model.predict([one_q])
print(prediction)
target_name = ['spam', 'not spam']
# print('actual: ', y_test)
print('prediction: ', target_name[prediction[0]])
# print('proba: ', proba)
# print('acc: ', acc)
