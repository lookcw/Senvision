import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.ensemble import RandomForestClassifier

from nltk.classify import ClassifierI
from statistics import mode
import csv
import ast
import numpy as np
import sys
import os
import datetime

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

#accept whether to interpret tweets or news
n = 1
data_type=""
for argument in sys.argv[1:]:
  if (argument == "-type"):
    data_type= sys.argv[n+1]
  if argument == "-iden":
    identifier = sys.argv[n+1]  
  n+=1

if data_type!="tweet" and data_type!="news":
  print "set -type to tweet or news"
  sys.exit(0)
if identifier == "default identifier":
  print "error: put in identifier with -iden arg"
  sys.exit(0)

if data_type=="tweet":
  data_dir="tweet_exist_descriptors"
if data_type=="news":
  data_dir="news_exist_descriptors"
now = datetime.datetime.now()
results_file=open('../Results/NLTK_results.csv','a')
result_writer=csv.writer(results_file,delimiter=',')
files = os.walk(data_dir).next()[2]
if identifier!=0:
  result_writer.writerow([now,identifier])

for file in files:
  comp_name=file.split("_")[0]
  print comp_name
  descriptor_file=open(data_dir+"/"+file,'r')
  descriptor_reader=csv.reader(descriptor_file,delimiter='\t')
  featuresets=list(descriptor_reader)
  for x in range(len(featuresets)):
    featuresets[x][0]=ast.literal_eval(featuresets[x][0])
    if featuresets[x][1]=="=":
      featuresets[x][1]="-"
  num_folds=10
  elements=len(featuresets)
  normal_acc=[]
  for i in range(0,num_folds):
    first_index=int((i*elements/float(num_folds)))
    second_index=int(((i+1)*elements/float(num_folds)))
    training_set=featuresets[:first_index]+featuresets[second_index:]
    testing_set=featuresets[first_index:second_index]


    classifier=nltk.NaiveBayesClassifier.train(training_set)
    #print("NaiveBayes_classifier accuracy percent:", (nltk.classify.accuracy(NaiveBayes_classifier, testing_set))*100)
    # print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
    # classifier.show_most_informative_features(15)

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)

    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier.train(training_set)
    RandomForest_classifier = SklearnClassifier(RandomForestClassifier())
    RandomForest_classifier.train(training_set)

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(training_set)

    SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    SGDClassifier_classifier.train(training_set)

    SVC_classifier = SklearnClassifier(SVC())
    SVC_classifier.train(training_set)

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)

    # NuSVC_classifier = SklearnClassifier(NuSVC())
    # NuSVC_classifier.train(training_set)

    voted_classifier = VoteClassifier(#SVC_classifier,
      LinearSVC_classifier,
                                      SGDClassifier_classifier,
                                      LogisticRegression_classifier)
    normal_acc.append((nltk.classify.accuracy(RandomForest_classifier, testing_set))*(len(testing_set)/float(elements)))
    print("voted_classifier accuracy percent:", (nltk.classify.accuracy(RandomForest_classifier, testing_set))*100)
  print sum(normal_acc)
  if identifier!=0:
    result_writer.writerow([comp_name,sum(normal_acc)])
# print("Classification:", voted_classifier.classify(testing_set[0][0]), "Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[1][0]), "Confidence %:",voted_classifier.confidence(testing_set[1][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[2][0]), "Confidence %:",voted_classifier.confidence(testing_set[2][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[3][0]), "Confidence %:",voted_classifier.confidence(testing_set[3][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[4][0]), "Confidence %:",voted_classifier.confidence(testing_set[4][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[5][0]), "Confidence %:",voted_classifier.confidence(testing_set[5][0])*100)