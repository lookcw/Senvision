from sklearn import datasets
from sklearn import svm
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import LabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
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

rng=np.random.RandomState(0)
X=rng.rand(10,2000)
X=np.array(X,dtype='float32')

clf.fit(iris.data, iris.target_names[iris.target])
print iris.target
print list(clf.predict(iris.data[:3]))

X=[[1,2],[2,4],[4,5],[3,2],[3,1]]
y=[0,0,1,1,2]

#predicts with 1 2d array on a 1d array
classif=OneVsRestClassifier(estimator=svm.SVC(random_state=0))
print classif.fit(X,y).predict(X)

Y=LabelBinarizer().fit_transform(y)
print classif.fit(X,Y).predict(X)


#can predict with different size descriptors
y=[[0,1],[0,2],[1,3],[0,2,3],[2,4]]
y=MultiLabelBinarizer().fit_transform(y)
print classif.fit(X,y).predict(X)

#s=pickle.dump(clf)
#clf2=pick.loads(s)
#print digits.data.shape
#print iris.data.shape
#print digits.target.shape
