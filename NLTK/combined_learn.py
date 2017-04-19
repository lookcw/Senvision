import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from nltk.classify import ClassifierI
from statistics import mode
import csv
import ast
import numpy as np
import sys
import os
import datetime
import codecs

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
        conf = choice_votes / float(len(votes))
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
  print "set -type to tweet or news or tweet_NER or news_NER_descriptors"
  sys.exit(0)


#setting types of data accepted to determine what folder to get descriptors from. 
if data_type=="news":
  data_dir="news_NER_descriptors"
  predictions_file=open("../Results/NLTK_News_predictions.csv",'w')
if data_type=="tweet":
  data_dir="twitter_NER_descriptors"
  predictions_file=open('../Results/NLTK_Tweet_predictions.csv','w')
now = datetime.datetime.now()

#open prediction and results file to write to
results_file=open('../Results/NLTK_results.csv','a')
result_writer=csv.writer(results_file,delimiter=',')
files = os.walk(data_dir).next()[2]

predictions_writer=csv.writer(predictions_file,delimiter=',')
predictions_writer.writerow(["date","symbol","Pred","Conf"])
#write identifier at start of results file
if identifier!="0":
  result_writer.writerow([now,identifier])
predictions=[]
#perform cross validation
for file in files:
  comp_name=file.split("_")[0]
  print comp_name

  #get descriptor data from files
  descriptor_file=open(data_dir+"/"+file,'r')
  descriptor_reader=csv.reader(descriptor_file,delimiter='\t')
  featuresets=list(descriptor_reader)
  print featuresets[0][0]
  for x in range(len(featuresets)):
    featuresets[x][1]=ast.literal_eval(featuresets[x][1])
    if featuresets[x][-1]=="=":
      featuresets[x][-1]="-"
  num_folds=10
  elements=len(featuresets)
  normal_acc=[]
  #calculate indicies to split by for cross validaton
  for i in range(0,num_folds):
    first_index=int((i*elements/float(num_folds)))
    second_index=int(((i+1)*elements/float(num_folds)))
    testing_set=[]
    training_set=[]
    dates=[]
    blind_testing_set=[]
    true=[]
    #split the sets into training and testing sets
    for n in (featuresets[:first_index]+featuresets[second_index:]):#adding training data and +/- for 
      training_set.append([dict(n[1]),n[2]])
    for n in (featuresets[first_index:second_index]):
      testing_set.append([n[1],n[2]])
      dates.append(n[0])

    for n in testing_set:
      blind_testing_set.append(n[0])
      true.append(n[1])
      #train data

    ##classifier=nltk.NaiveBayesClassifier.train(training_set)
    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)

    #Maxent_classifier = SklearnClassifier(MaxentClassifier())
    #Maxent_classifier.train(training_set)

    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier.train(training_set)

    RandomForest_classifier = SklearnClassifier(RandomForestClassifier(n_estimators=100))
    RandomForest_classifier.train(training_set)

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(training_set)

    SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    SGDClassifier_classifier.train(training_set)

    SVC_classifier = SklearnClassifier(SVC(kernel='rbf'))
    SVC_classifier.train(training_set)

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)

    NearestNeighbors_classifier=SklearnClassifier(KNeighborsClassifier(n_neighbors=2, algorithm='ball_tree'))
    NearestNeighbors_classifier.train(training_set)

    # NuSVC_classifier = SklearnClassifier(NuSVC())
    # NuSVC_classifier.train(training_set)
    voted_classifier = VoteClassifier(
        RandomForest_classifier,
                                        SGDClassifier_classifier,
                                        LogisticRegression_classifier,BernoulliNB_classifier,MNB_classifier,NearestNeighbors_classifier,SVC_classifier)
    normal_acc.append((nltk.classify.accuracy(voted_classifier, testing_set))*(len(testing_set)/float(elements)))
    print len(testing_set)
    plusminus=voted_classifier.classify_many(blind_testing_set)

    for i in range(len(dates)):
      predictions.append([dates[i],comp_name,str(plusminus[i]),voted_classifier.confidence(blind_testing_set[i])])  
      #predictions_writer.writerow([dates[i],comp_name,str(plusminus[i])])
      print [plusminus[i],true[i]]

      
      #print predictions
    print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)
  print sum(normal_acc)
  if identifier!=0:
    result_writer.writerow([comp_name,sum(normal_acc)])

    # print("Classification:", voted_classifier.classify(testing_set[0][0]), "Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[1][0]), "Confidence %:",voted_classifier.confidence(testing_set[1][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[2][0]), "Confidence %:",voted_classifier.confidence(testing_set[2][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[3][0]), "Confidence %:",voted_classifier.confidence(testing_set[3][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[4][0]), "Confidence %:",voted_classifier.confidence(testing_set[4][0])*100)
# print("Classification:", voted_classifier.classify(testing_set[5][0]), "Confidence %:",voted_classifier.confidence(testing_set[5][0])*100)


##########################################################
#####Figuring out percentage to invest per comp###########
##########################################################

totals={} #dictionary to store totals per day.
percentages={}
for i in predictions:
  if i[2]=="+":
    if i[0] in totals:
      totals[i[0]]+=i[-1]
    else:
      totals[i[0]]=i[-1]
for i in predictions:
  if i[2]=="+":
    if i[0] in percentages:
      percentages[i[0]].append([i[0],i[1],i[2],i[-1]/totals[i[0]]])
    else:
      percentages[i[0]]=[[i[0],i[1],i[2],i[-1]/totals[i[0]]]]
  else:
    if i[0] in percentages:
      print i[0] in percentages
      percentages[i[0]].append([i[0],i[1],i[2],0])
    else:
      percentages[i[0]]=[[i[0],i[1],i[2],0]]

print percentages


for i in percentages:
  for k in percentages[i]:
    predictions_writer.writerow(k)
