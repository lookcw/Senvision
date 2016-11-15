import os
import csv
from datetime import date, timedelta as td
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

allvalues = {}

##########################################################
############## open files containing words ###############
##########################################################

good_words = open("Vocab/goodwords.txt", "r")
bad_words =  open("Vocab/badwords.txt", "r")

good_clusters = open("Vocab_Clusters/goodwords_clustered.txt", "r")
bad_clusters = open("Vocab_Clusters/badwords_clustered.txt", "r")


###########################################################
#append all the words and their contexts to various arrays#
###########################################################
good_arr = []
bad_arr = []

good_clusters_arr = []
bad_clusters_arr = []


##############################################
########## READING INDIVIDUAL WORDS ##########
##############################################
reader = csv.reader(good_words, delimiter="\n")
for row in reader:
	good_arr.append(row[0])
for word in good_arr:
	if word == '':
		good_arr.remove(word)

reader = csv.reader(bad_words, delimiter = "\n")
for row in reader:
	bad_arr.append(row[0])
for word in bad_arr:
        if word == '':
                bad_arr.remove(word) 


###################################################
############## READING CLUSTERS ###################
###################################################
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
full_company_names = ['Apple', 'Boeing', 'Google', 'Intel', 'Merck', 'Morgan Chase', 'p&g', 'Walmart']
#full_company_names = open("file_containing_company_names.txt", "r")
dates = []

##########################################################################################
###                         loop through all the companies                             ### 
##########################################################################################
#outf = open('./descriptors/DESCRIPTORS.txt', 'w')
#outf.write('DATE' + '\t' + 'COMPANY' + '\t')
count = 0
for cluster in good_clusters_arr:
	count+=1
for cluster in bad_clusters_arr:
	count+=1
cluster_count = count


for company_name in full_company_names:

	outf = open('./descriptors/' + company_name + '_descriptor.tsv', 'w')
	outf.write('DATE' + '\t' + 'COMPANY' + '\t') 
	for i in range(0, cluster_count):
		outf.write("Cluster_" + str(i+1) + "\t")
	outf.write('\n')

	for filename in os.listdir('AllTweets/filteredTweets/' + company_name):
		index1 = filename.index('_')
		index2 = filename.index('T')
		date = filename[index1+1:index2]

		outf.write(str(date) + "\t" + str(company_name) + "\t")

		num_features = 40 #subject to change
		min_word_count = 1 #subject to change
		num_workers = 15 #should be good
		context = 10 #subject to change
		#downsampling = 1e-3

		sentences = LineSentence('AllTweets/filteredTweets/' + company_name + '/'  + filename)

		posarr = []
		negarr = []

		for word in good_arr:
			allvalues[str(company_name) + "_" + str(word)] = 0
		for word in bad_arr:
			allvalues[str(company_name) + "_" + str(word)] = 0

		good_count = 0
		bad_count = 0
		for sentence in sentences:
			for word in sentence:
				if word in good_arr:
					good_count += 1
					allvalues[str(company_name) + "_" + str(word)] += 1
				elif word in bad_arr:
					bad_count += 1
					allvalues[str(company_name) + "_" + str(word)] += 1
				
		print("Count of good words", good_count)
		print("Count of bad words", bad_count)
		print("Total count is:", good_count+bad_count)

######################################################################################################
################                      GENERATING DESCRIPTORS                       ###################
######################################################################################################
		DESCRIPTOR = []
		for cluster in good_clusters_arr:
			count = 0
			cluster_avg = 0
			for x in cluster:
#				print("word in cluster:", x)
				if allvalues[str(company_name) + "_" + str(x)] != 0:
					count+=1
					cluster_avg += allvalues[str(company_name) + "_" + str(x)]
			print("What the descriptor is", cluster_avg)
			DESCRIPTOR.append(cluster_avg)

                for cluster in bad_clusters_arr: 
                        count = 0
                        cluster_avg = 0 
                        for x in cluster:
                                if allvalues[str(company_name) + "_" + str(x)] != 0:
                                        count+=1
                                        cluster_avg += allvalues[str(company_name) + "_" + str(x)]
                        print("What the descriptor is", cluster_avg)
                        DESCRIPTOR.append(cluster_avg)

	
		for value in DESCRIPTOR:
			outf.write(str(value) + '\t')
		outf.write('\n')
