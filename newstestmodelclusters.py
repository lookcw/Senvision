import os
import csv
from datetime import date, timedelta as td
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

allvalues = {}

##########################################################
# open files containing words ############################
##########################################################

good_words = open("Vocab/good_words.txt", "r")
bad_words =  open("Vocab/bad_words.txt", "r")

good_clusters = open("Vocab_Clusters/good_words_clustered.txt", "r")
bad_clusters = open("Vocab_Clusters/bad_words_clustered.txt", "r")

###########################################################
#append all the words and their contexts to various arrays#
###########################################################
good_arr = []
bad_arr = []

good_clusters_arr = []
bad_clusters_arr = []

##############################################
# READING INDIVIDUAL WORDS ###################
##############################################
reader = csv.reader(good_words, delimiter=" ")
for row in reader:
	for item in row:
		good_arr.append(item)
for word in good_arr:
	if word == '':
		good_arr.remove(word)

reader = csv.reader(bad_words, delimiter = " ")
for row in reader:
	for item in row:
		bad_arr.append(item)
for word in bad_arr:
        if word == '':
                bad_arr.remove(word) 

##############################################
###            READING CLUSTERS            ###
##############################################
reader = csv.reader(good_clusters, delimiter = " ")
for row in reader:
	good_clusters_arr.append(row)
for cluster in good_clusters_arr:
	for word in cluster:
		if word == '':
			cluster.remove(word)

reader = csv.reader(bad_clusters, delimiter = " ")
for row in reader:
	bad_clusters_arr.append(row)
for cluster in bad_clusters_arr:
        for word in cluster:
                if word == '':
                        cluster.remove(word) 


class MySentences(object):
	def __init__ (self,dirname):
		self.dirname = dirname
	def __iter__ (self):
		for fname in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname,fname)):
				yield line.split()


######################################################################################################
###                            COMPANY_NAMES AND DATE COLLECTION                                   ###
######################################################################################################
#full_company_names = ['Apple', 'Boeing', 'Google', 'Intel', 'Merck', 'JPMorgan Chase', 'Procter & Gamble', 'Walmart']
#full_company_names = [name for name in os.listdir("News/ArticlesData") if os.path.isdir(name)]
full_company_names = []
#full_company_names = ['JPMorgan Chase']
for name in os.listdir("News/ArticlesData/"):
	full_company_names.append(name)
#print(full_company_names)
dates = []


##########################################################################################
###                         loop through all the companies                             ### 
##########################################################################################
count = 0
#print(good_words)
#print(bad_words)
#print(good_clusters_arr)
#print(bad_clusters_arr)
for cluster in good_clusters_arr:
	count+=1
for cluster in bad_clusters_arr:
	count+=1
#for cluster in neutral_clusters_arr:
#	for cluster in neutral_good_clusters_arr:
#		count+=1
#	for cluster in neutral_bad_clusters_arr: 
#		count+=1
#for i in range(0, count):
#	outf.write("Cluster_" + str(i) + "\t")
#outf.write('\n')

cluster_count = count
print("NUMBER OF CLUSTERS", cluster_count)

#for company_name in full_company_names:
#	count=0
#	for filename in os.listdir('News/ArticlesData/' + company_name):
#		count+=1
#	print(company name, count)

for company_name in full_company_names:
	if company_name == 'JPMorgan Chase':
		company_string = 'J.P. Morgan'
	elif company_name == 'Procter & Gamble':
		company_string = 'Procter'
	elif company_name == 'INTC':
		company_string = 'Intel'
	else:
		company_string = company_name
	outf = open('./descriptors/' + company_name + '_descriptor.tsv', 'w')
	outf.write('DATE' + '\t' + 'COMPANY' + '\t') 
	for i in range(0, cluster_count):
		outf.write('Cluster_' + str(i+1) + '\t')
	outf.write('\n')

	for filename in os.listdir('News/ArticlesData/' + company_name):
		print("looping through news articles...")
		index1 = filename.index('_')
		index2 = filename.rfind('A')
		date = filename[(index1+1):(index2-1)]
#		print(date)
		outf.write(str(date) + "\t" + str(company_name) + "\t")

		num_features = 40 #subject to change
		min_word_count = 1 #subject to change
		num_workers = 15 #should be good
		context = 10 #subject to change
		#downsampling = 1e-3

		sentences = LineSentence('News/ArticlesData/' + company_name + '/'  + filename)
#		print ('News/ArticlesData/' + company_name + '/'  + filename)
		
		print("Training model...")
		model = word2vec.Word2Vec(sentences, workers=num_workers, size=num_features, min_count=min_word_count, window=context)
 	
		posarr = []
		negarr = []
		print("made it here")

		for x in good_arr:
			#print("...but not here")
			#print("Good word: ", x)
			try:
				dist = model.similarity(str(company_string), x)
				print(dist)
				posarr.append(dist)
				allvalues[str(company_name) + "_" + str(x)] = dist
			except KeyError:
				print("no distance found for", x)
				allvalues[str(company_name) + "_" + str(x)] = 0
				continue

		for x in bad_arr:
			try:
				dist = model.similarity(str(company_string), x) 
				print(dist)
				negarr.append(dist)
				allvalues[str(company_name) + "_" + str(x)] = dist 
			except KeyError:
				print("no distance found for", x)
				allvalues[str(company_name) + "_" + str(x)] = 0
				continue


######################################################################################################
################                      GENERATING DESCRIPTORS                       ###################
######################################################################################################
		DESCRIPTOR = []
		for cluster in good_clusters_arr:
			count = 0
			cluster_avg = 0
			for x in cluster:
			#	print("word in cluster:", x)
				if x!= 0:
					count+=1
					cluster_avg += allvalues[str(company_name) + "_" + str(x)]
			cluster_avg /= count
			DESCRIPTOR.append(cluster_avg)

                for cluster in bad_clusters_arr: 
                        count = 0
                        cluster_avg = 0 
                        for x in cluster:
			#	print("word in cluster:", x) 
                                if x!= 0:
                                        count+=1
                                        cluster_avg += allvalues[str(company_name) + "_" + str(x)]
                        cluster_avg /= count
                        DESCRIPTOR.append(cluster_avg)

		
		for value in DESCRIPTOR:
			outf.write(str(value) + '\t')
		outf.write('\n')	
