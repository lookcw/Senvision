from __future__ import division
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

good_words = open("Vocab/good_words.txt", "r")
bad_words =  open("Vocab/bad_words.txt", "r")
correlated_words = open("finalwords.txt", "r")

#good_clusters = open("Vocab_Clusters/goodwords_clustered.txt", "r")
#bad_clusters = open("Vocab_Clusters/badwords_clustered.txt", "r")


###########################################################
#append all the words and their contexts to various arrays#
###########################################################
good_arr = []
bad_arr = []
correlated_arr = []
good_correlated_arr = []
bad_correlated_arr = []

#good_clusters_arr = []
#bad_clusters_arr = []


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

reader = csv.reader(correlated_words, delimiter = "\n")
for row in reader:
	correlated_arr.append(row[0])
for word in correlated_arr:
	if word == '':
		correlated_arr.remove(word)

for word in correlated_arr:
	if word in good_arr:
		good_correlated_arr.append(word)
	elif word in bad_arr:
		bad_correlated_arr.append(word)


###################################################
############## READING CLUSTERS ###################
###################################################
#reader = csv.reader(good_clusters, delimiter = " ")
#for row in reader:
# 	good_clusters_arr.append(row)
# for cluster in good_clusters_arr:
# 	for word in cluster:
# 		if word == '':
# 			cluster.remove(word)

# reader = csv.reader(bad_clusters, delimiter = " ")
# for row in reader:
# 	bad_clusters_arr.append(row)
# for cluster in bad_clusters_arr:
#         for word in cluster:
#                 if word == '':
#                         cluster.remove(word)

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
#for cluster in good_clusters_arr:
#	count+=1
#for cluster in bad_clusters_arr:
#	count+=1
#cluster_count = count


for company_name in full_company_names:

	outf = open('./descriptors/' + company_name + '_descriptor.tsv', 'w')
	outf.write('DATE' + '\t' + 'COMPANY' + '\t') 
	for word in good_correlated_arr:
		outf.write(word + "\t")
	for word in bad_correlated_arr:
		outf.write(word + "\t")
	#for i in range(0, cluster_count):
	#	outf.write("Cluster_" + str(i+1) + "\t")
	outf.write('\n')

	for filename in os.listdir('../AllTweets/filteredTweets/' + company_name):
		index1 = filename.index('_')
		index2 = filename.index('T')
		date = filename[index1+1:index2]

		outf.write(str(date) + "\t" + str(company_name) + "\t")

		sentences = LineSentence('../AllTweets/filteredTweets/' + company_name + '/'  + filename)
		file = open(('../AllTweets/filteredTweets/' + company_name + '/'  + filename), 'rU')
		reader = csv.reader(file, dialect=csv.excel_tab)
		tweetcount = len(list(reader))

		posarr = []
		negarr = []

		for word in good_correlated_arr:
			allvalues[str(company_name) + "_" + str(word)] = 0
		for word in bad_correlated_arr:
			allvalues[str(company_name) + "_" + str(word)] = 0


		for sentence in sentences:
			for word in sentence:
				if word in good_correlated_arr:
					allvalues[str(company_name) + "_" + str(word)] += 1
				elif word in bad_correlated_arr:
					allvalues[str(company_name) + "_" + str(word)] += 1

		for x in allvalues:
			allvalues[x] = allvalues[x]/tweetcount
		print(allvalues)
				

######################################################################################################
################                      GENERATING DESCRIPTORS                       ###################
######################################################################################################
		DESCRIPTOR = []
		for word in good_correlated_arr:
			DESCRIPTOR.append(allvalues[company_name + "_" + word])
		for word in bad_correlated_arr:
			DESCRIPTOR.append(allvalues[company_name + "_" + word])
	
		for value in DESCRIPTOR:
			outf.write(str(value) + '\t')
		outf.write('\n')
