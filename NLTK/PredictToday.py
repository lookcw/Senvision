#returns a file with the predictions of the next three days of the given companies whether they will go up or down.
import datetime
from datetime import timedelta
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
	output_descriptors="Future_Predictions/Tweet_Predictions" #the folder the desciptors will be put into.
	descriptor_dir="twitter_NER_descriptors"
if data_type=="news":
	data_dir='../News/ArticlesData'
	common_words_file="News_Common_NER"
	output_descriptors="Future_Predictions/News_Predictions"
	descriptor_dir="news_NER_descriptors"

##########################Picking recent dates#########################
now = datetime.datetime.now()
day2before=now-timedelta(days=2)
day3before=now-timedelta(days=3)




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
				k=w in entity_names
				features[w]=k
			######################################write nltk results######################################
			descriptors.append([date,features])
			descriptor_writer.writerow([date,features])

#			print filename+" does not exist"


for subdir in subdirs[1:]:
	find_features_comp(subdir)
# Print all entity names





#################################################################
######################sklearn predictions########################
#################################################################






files = os.walk(descriptor_dir).next()[2]
predictions_file=open('../Results/NLTK_predictions.csv','w')
predictions_writer=csv.writer(predictions_file,delimiter=',')
predictions_writer.writerow(["date","symbol","Pred"])
#write identifier at start of results file


#perform cross validation
for file in files:
  comp_name=file.split("_")[0]
  print comp_name

  #get descriptor data from files
  descriptor_file=open(descriptor_dir+"/"+file,'r')
  descriptor_reader=csv.reader(descriptor_file,delimiter='\t')
  featuresets=list(descriptor_reader)
  print featuresets[0][0]
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
    for n in (featuresets[:first_index]+featuresets[second_index:]):#adding training data and +/- for 
      training_set.append([dict(n[1]),n[2]])
    for n in (featuresets[first_index:second_index]):
      testing_set.append([n[1],n[2]])
      dates.append(n[0])



    for n in testing_set:
      blind_testing_set.append(n[0])
      true.append(n[1])
#train data

    classifier=nltk.NaiveBayesClassifier.train(training_set)

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

    #SVC_classifier = SklearnClassifier(SVC())
    #SVC_classifier.train(training_set)

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)

    # NuSVC_classifier = SklearnClassifier(NuSVC())
    # NuSVC_classifier.train(training_set)

    voted_classifier = VoteClassifier(
      RandomForest_classifier,
                                      SGDClassifier_classifier,
                                      LogisticRegression_classifier,BernoulliNB_classifier,MNB_classifier)
    normal_acc.append((nltk.classify.accuracy(voted_classifier, testing_set))*(len(testing_set)/float(elements)))
    print len(testing_set)
    plusminus=voted_classifier.classify_many(blind_testing_set)
    predictions=[]

    for i in range(len(dates)):
      predictions.append([dates[i],comp_name,str(plusminus[i])])
      predictions_writer.writerow([dates[i],comp_name,str(plusminus[i])])
      print [plusminus[i],true[i]]


    #print predictions