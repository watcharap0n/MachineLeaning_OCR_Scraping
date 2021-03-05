from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import datasets
import numpy as np


class FeatureIris:
    def __init__(self, dataset):
        self.dataset = dataset

    def iris_tree(self, data_test):
        iris = self.dataset
        test_idx = [0, 50, 100]
        train_target = np.delete(iris.target, test_idx)
        train_data = np.delete(iris.data, test_idx, axis=0)
        data_idx = data_test
        test_data = np.array(([data_idx]))
        clf = tree.DecisionTreeClassifier()
        clf.fit(train_data, train_target)
        prediction = clf.predict(test_data)
        return prediction

    def iris_train_tree(self, data_test, acc):
        iris = self.dataset
        x = iris.data
        y = iris.target
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.5)
        my_classifier = tree.DecisionTreeClssifier()
        my_classifier.fit(x_train, y_train)
        idx = data_test
        test_data = np.array([idx])
        predictions = my_classifier.predict(test_data)
        result = accuracy_score(acc, predictions)
        return predictions, result

    def iris_train_knn(self, data_test):
        iris = self.dataset
        x = iris.data
        y = iris.target
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.5)
        my_classifier = KNeighborsClassifier()
        my_classifier.fit(x_train, y_train)
        idx = data_test
        test_data = np.array([idx])
        predictions = my_classifier.predict(test_data)
        result = accuracy_score(y_test, predictions)
        return predictions, result


