import nltk
import random
from nltk.corpus import movie_reviews
from nltk.tokenize import word_tokenize
import os
import io
import csv
import codecs


# documents = [(list(movie_reviews.words(fileid)), category)
#              for category in movie_reviews.categories()
#              for fileid in movie_reviews.fileids(category)]

# print movie_reviews.words('neg/cv000_29416.txt')
# print type (movie_reviews.words('neg/cv000_29416.txt'))
# random.shuffle(documents)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

article_dir = '../News/ArticlesData'

num_common_words=3000                                                                                                                    
subdirs = [x[0] for x in os.walk(article_dir)]                                                                            
# for subdir in subdirs:     
# 	all_words=[]
# 	files = os.walk(subdir).next()[2]
# 	if (len(files) > 0):
# 		for file in files:
# 			filename=subdir + "/" + file
# 			file = file.replace('+', '\+')
# 			print file
# 			corpusReader = nltk.corpus.PlaintextCorpusReader(subdir,file)
# 			comp=file.split('_')[0]
# 			date = file.split('_')[2]
# 			for w in corpusReader.words():
# 				if is_ascii(w):
# 					all_words.append(w.lower())
# 	all_words = nltk.FreqDist(all_words)
# 	print type(all_words)
# 	word_features = [x[0] for x in all_words.most_common(3000)]
# 	write_file=open("News_Common_words/"+subdir.split("/")[-1]+"_top_"+str(num_common_words)+"_words.tsv",'w')
# 	writer=csv.writer(write_file,delimiter='\t')
# 	writer.writerow(word_features)


def find_features_comp(subdir):
	print subdir
	comp=subdir.split("/")[-1]
	files = os.walk(subdir).next()[2]
	#######opening files per comp
	stock_file=open("../stock_data/tweet_date_data/"+comp+"_cleaned.tsv",'r')
	stock_reader=csv.reader(stock_file,delimiter='\t')
	common_words=open("News_Common_words/"+comp+"_top_"+str(num_common_words)+"_words.tsv",'r')
	word_reader=csv.reader(common_words,delimiter='\t')
	descriptor_file=open("news_exist_descriptors/"+comp+"_descriptor.tsv",'w')
	descriptor_writer=csv.writer(descriptor_file,delimiter='\t')
	word_features=next(word_reader)
	stock_lines=list(stock_reader)
	stock_dict={}
	descriptors=[]
	for line in stock_lines:
		stock_dict[line[1]]=line[-2]
	if (len(files) > 0): 
		for file in files:
			all_words=[]
			filec = file.replace('+', '\+')
			corpusReader = nltk.corpus.PlaintextCorpusReader(subdir,filec)
			for w in corpusReader.words():
				if is_ascii(w):
 					all_words.append(w.lower())
 			all_words = nltk.FreqDist(all_words)
			date = file.split('_')[1]
			with codecs.open(subdir+"/"+file,'r',encoding='utf8') as f:
				tweet_words = f.read()
			words=word_tokenize(tweet_words)
			features = {}
			for w in word_features:
				k=w in words
				features[w]=k
				#features[w] = (all_words[w])
			if date in stock_dict:
				descriptors.append([features,stock_dict[date]])
				descriptor_writer.writerow([features,stock_dict[date]])

for subdir in subdirs[1:]:
	find_features_comp(subdir)

        	

	
#featuresets = [(find_features(rev), category) for (rev, category) in documents]

