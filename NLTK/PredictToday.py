#returns a file with the predictions of the next three days of the given companies whether they will go up or down.
import datetime
from datetime import timedelta as td
from dateutil.parser import parse
import os
import sys
import csv
import codecs
import nltk

from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.ensemble import RandomForestClassifier
#from sklearn.gaussian_process import GuassianProcessClassifier
from sklearn.neighbors import KNeighborsClassifier


import ast

from nltk.classify import ClassifierI
from statistics import mode


#returns array of entity names in a string
def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names


#############################inputting data########################
n=1
for argument in sys.argv[1:]:
  if (argument == "-type"):
    data_type= sys.argv[n+1]
  n+=1
if ((data_type!="tweet" and data_type!="news")):
	print "Set -type to 'tweet' or 'news'"

if data_type=="tweet":
	data_dir='../AllTweets/filteredTweets' #the tweet data
	common_words_file="Tweet_Common_NER" #the tweet common words from the above 
	output_descriptors="Future_Predictions/Tweet_descriptors" #the folder the desciptors will be put into.
	descriptor_dir="twitter_NER_descriptors"
	predictions="Twitter_Future_Predictions.tsv"
if data_type=="news":
	data_dir='../News/ArticlesData'
	common_words_file="News_Common_NER"
	output_descriptors="Future_Predictions/News_descriptors"
	descriptor_dir="news_NER_descriptors"
	predictions="Twitter_Future_Predictions.tsv"

##########################Picking recent dates#########################
now = datetime.datetime.now()
day2before=now-td(days=2)
day3before=now-td(days=3)




recents=[day2before,day3before]
num_common_words=1000
subdirs = [x[0] for x in os.walk(data_dir)]



def find_features_comp(subdir):
	comp=subdir.split("/")[-1]
	files = os.walk(subdir).next()[2]
	stock_dict={}
	descriptors=[]


	#######opening files per comp
	stock_file=open("../stock_data/tweet_date_data/"+comp+"_cleaned.tsv",'r')
	stock_reader=csv.reader(stock_file,delimiter='\t') #reader for the stock data file
	common_words=open(common_words_file+"/"+comp+"_top_"+str(num_common_words)+"_words.tsv",'r')
	word_reader=csv.reader(common_words,delimiter='\t')#reader for common words
	descriptor_file=open(output_descriptors+"/"+comp+"_future_descriptor.tsv",'w')
	descriptor_writer=csv.writer(descriptor_file,delimiter='\t')
	word_features=next(word_reader) #the common words 

	for line in stock_reader:
		stock_dict[line[1]]=line[-2]


	#set key of date equal to value of +/-
	# for line in stock_lines:
	# 	stock_dict[line[1]]=line[-2]
	# 	print line[1]
	print len(stock_dict)
	#create descriptors and add value to end
	if (len(files) > 0): 
		for date in recents:	
			entity_names=[]
			file=""
			if(data_type=="tweet"):
				filename=os.path.join(subdir,comp+"_"+str(date.date())+"Tweets.txt")
			if(data_type=="news"):
				filename=os.path.join(subdir,comp+"_"+str(date.date())+"_Articles.txt")
			try:
				with codecs.open(filename, 'r','latin-1') as f:
						sample = f.read()
				print "went into try "
				print filename
				print "helllo"
				#####################################start nltk analysis######################################
				sentences = nltk.sent_tokenize(sample)
				tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
				tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
				chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
				for tree in chunked_sentences:
				    entity_names.extend(extract_entity_names(tree))
				features = {}
				for w in word_features:
					#print w in entity_names
					k=w in entity_names
					features[w]=k
				######################################write nltk results######################################
				descriptors.append([date.date(),features])
				descriptor_writer.writerow([date.date(),features])
			except:
				filename+ " doesnt exist"

#			print filename+" does not exist"


for subdir in subdirs[1:]:
	find_features_comp(subdir)
# Print all entity names





#################################################################
######################sklearn predictions########################
#################################################################


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


files = os.walk(output_descriptors).next()[2]
predictions_file=open('../Results/Future_Predictions.csv','w')
predictions_writer=csv.writer(predictions_file,delimiter=',')
predictions_writer.writerow(["date","symbol","Pred","Conf"])
#write identifier at start of results file
predictions=[]

#perform cross validation
for file in files:
	comp_name=file.split("_")[0]
	print comp_name

	#get descriptor data from files
	training_descriptor_file=open(descriptor_dir+"/"+comp_name+"_descriptor.tsv",'r')
	training_descriptor_reader=csv.reader(training_descriptor_file,delimiter='\t')
	testing_descriptor_file=open(output_descriptors+"/"+file,'r')
	testing_descriptor_reader=csv.reader(testing_descriptor_file,delimiter='\t')
	featuresets=list(training_descriptor_reader)
	test_featuresets=list(testing_descriptor_reader)
	training_descriptor_file.close()	
	for x in range(len(featuresets)):
		featuresets[x][1]=ast.literal_eval(featuresets[x][1])
		if featuresets[x][-1]=="=":
		  featuresets[x][-1]="-"
	elements=len(featuresets)
	normal_acc=[]

	testing_set=[]
	training_set=[]
	dates=[]

	#split the sets into training and testing sets
	for n in (featuresets):#adding training data and +/- for 
		training_set.append([dict(n[1]),n[2]])
	for line in test_featuresets:
		testing_set.append(n[1])
	#train data

	classifier=nltk.NaiveBayesClassifier.train(training_set)

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
	print len(testing_set)
	plusminus=voted_classifier.classify_many(testing_set)
	#print LinearSVC_classifier.prob_classify_many(testing_set)
	#print SGDClassifier_classifier.prob_classify_many(testing_set)
	#k=LogisticRegression_classifier.prob_classify_many(testing_set)
	total_conf=0.0
	for k in testing_set:
		voted_classifier.confidence(k)

	#puts predictions in filecd 
	for i in range(len(test_featuresets)):
		date=parse(test_featuresets[i][0])
		date+=td(days=3)
		#datetime.datetime.today().strftime('%Y-%m-%d')
		#print date
		predictions.append([date.strftime('%Y-%m-%d'),comp_name,str(plusminus[i]),voted_classifier.confidence(testing_set[i])])
		
		print [date.strftime('%Y-%m-%d'), comp_name, plusminus[i],voted_classifier.confidence(testing_set[i])]

	#print predictions


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
			print i[0] in percentages
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