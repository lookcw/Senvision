import numpy as np
import os
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn import svm
import datetime
import csv
import sys
import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode


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
num_folds=5

MNB_classifier = SklearnClassifier(MultinomialNB())



BernoulliNB_classifier = SklearnClassifier(BernoulliNB())



LogisticRegression_classifier = SklearnClassifier(LogisticRegression())



SGDClassifier_classifier = SklearnClassifier(SGDClassifier())



##SVC_classifier = SklearnClassifier(SVC())
##SVC_classifier.train(train_data)
##print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())



NuSVC_classifier = SklearnClassifier(NuSVC())







for subdir, dirs, files in os.walk(descriptor_dir):
    for file in files:
	des_file=open(os.path.join(subdir, file),'r')
	reader=csv.reader(des_file,delimiter='\t')
	for i in range(0,num_folds):
		print "hi"
		first_index=int((i*elements/float(num_folds)))
		second_index=int(((i+1)*elements/float(num_folds)))
		test_data = array[first_index:second_index]
		train_data= np.concatenate([data[0:first_index],data[second_index:]],axis=0)
		print train_data
		train_target= np.concatenate([data[0:first_index],data[second_index:]])
		print "test_data.shape= ",test_data.shape," train_data.shape=",train_data.shape,"data.shape=",data.shape
		MNB_classifier.train(train_data)
		BernoulliNB_classifier.train(train_data)
		LinearSVC_classifier.train(train_data)
		SGDClassifier_classifier.train(train_data)
		LogisticRegression_classifier.train(train_data)
		NuSVC_classifier.train(train_data)
		print (len(train_data)+len(test_data))," ",len(data)


		print (nltk.classify(test_data))
		# print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
		# print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
		# print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
		# print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)
		# print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
		# print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)
	if identifier!="0":
		result_writer.writerow([comp_name,metrics.accuracy_score(target,predicted)])
	
	print comp_name+ ": "+ str(metrics.accuracy_score(target,predicted))
	

