from sklearn import datasets
from sklearn import svm
import pickle
from sklearn.externals import joblib
import numpy as np
from sklearn import random_projection
iris=datasets.load_iris()
digits=datasets.load_digits()
clf=svm.SVC(gamma=0.001,C=100.)
clf.fit(digits.data[:-1],digits.target[:-1])
print clf.predict(digits.data[-1:])
print digits.target[-1]
joblib.dump(clf,'../filename.pkl')


s=pickle.dump(clf)
clf2=pick.loads(s)
o
#print digits.data.shape
#print iris.data.shape
#print digits.target.shape
