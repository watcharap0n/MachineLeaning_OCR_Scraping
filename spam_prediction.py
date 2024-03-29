import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, scale, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_csv('datasets/data.csv')

x = data[['company', 'fname']].values
y = data[['class']]

lst = []
le = LabelEncoder()
q = ['Asava Property Group Co., Ltd.', 'Pornchanok Assavanives']
for i, e in zip(range(len(x[0])), q):
    x[:, i] = le.fit_transform(x[:, i].astype(str))
    lst.append(le.transform([e]))
    # print(le.inverse_transform(le.transform([e])))

data_one = [q[0] for q in lst]
print(le.inverse_transform(data_one))
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.4)
model = KNeighborsClassifier()
model = model.fit(x_train, y_train)
prediction = model.predict([data_one])
print(prediction)
# acc = accuracy_score(y_test, prediction)
target_name = ['not spam', 'spam']
print(target_name[prediction[0]])

X_train_pd = pd.DataFrame(x_train, columns=['x', 'y'])
y_train_pd = pd.DataFrame(y_train, columns=['class'])

df = pd.concat([X_train_pd, y_train_pd], axis=1)
df["class"] = df["class"].astype(str)
df.plot.scatter(x="x", y="y")
plt.show()
# plt.plot(df['y'], df['y'], 'ro')
# plt.axis([df['class']])
# plt.show()
# fig = px.scatter(df, x="x", y="y", color="class")
# fig.show()