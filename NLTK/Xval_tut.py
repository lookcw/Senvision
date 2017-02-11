import numpy as np
import os
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import datetime
import csv
import sys


descriptor_dir = '../CorrelationAnalysis/tweetdescriptors/'	
results_file=open('../Results/sklearn_results.csv','a')
result_writer=csv.writer(results_file,delimiter=',')
n = 1
identifier="default identifier"
for argument in sys.argv[1:]:
	if argument == "-iden":
		identifier = sys.argv[n+1]
	n+=1
	
if identifier == "default identifier":
	print "error: put in identifier with -iden arg"
	sys.exit(0)
now = datetime.datetime.now()
if identifier!="0":
	result_writer.writerow([now,identifier])
for subdir, dirs, files in os.walk(descriptor_dir):
    for file in files:
	des_file=open(os.path.join(subdir, file),'r')
	reader=csv.reader(des_file,delimiter='\t')
	array=np.array(list(reader))
	print array.shape
	comp_name=array[1][1]
	array=array[1:]#take out company names names
	data=array[:][:,2:-1] #extract the training data without target
	target=array[:][:,-1] #extract target
	#(X_train,X_test,y_train,y_test)=train_test_split(data,target,test_size=0.2,random_state=0)
	clf=svm.SVC(kernel='rbf',C=100,decision_function_shape=None) #create svm

	scores = cross_val_score(clf,data,target,cv=5,scoring='accuracy')#cv its number of folds 
	predicted=cross_val_predict(clf,data,target,cv=5)
	if identifier!="0":
		result_writer.writerow([comp_name,metrics.accuracy_score(target,predicted)])
	print comp_name+ ": "+ str(metrics.accuracy_score(target,predicted))
	

