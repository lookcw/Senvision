import nltk
import random
from nltk.corpus import movie_reviews
import os

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

print type(movie_reviews.words('neg/cv000_29416.txt'))
random.shuffle(documents)


descriptor_dir = '../AllTweets/filteredTweets'	

                                                                                                 
all_words=[]                                                                                         
subdirs = [x[0] for x in os.walk(descriptor_dir)]                                                                            
for subdir in subdirs:                                                                                            
    files = os.walk(subdir).next()[2]                                                                             
    if (len(files) > 0):                                                                                          
        for file in files:    
        	filename=subdir + "/" + file
        	filename = filename.replace('+', '\+')
        	corpusReader = nltk.corpus.PlaintextCorpusReader(filename)
        	date = filename.split('_')[1].replace('Tweets.txt', '').replace('Tweets+.txt', '')
        	for w in corpusReader.words():
				all_words.append(w.lower())


all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:3000]

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

for subdir in subdirs:                                                                                            
    files = os.walk(subdir).next()[2]                                                                             
    if (len(files) > 0):                                                                                          
        for file in files:
        	

	
#featuresets = [(find_features(rev), category) for (rev, category) in documents]

