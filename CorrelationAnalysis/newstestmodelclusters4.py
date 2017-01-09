from __future__ import division
import os
import csv
import nltk
from datetime import date, timedelta as td
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

allvalues = {}
stockdata_dict = {}

path = '../stock_data/tweet_date_data/'
pathcompany = '../News/ArticlesData/'
full_company_names = []
for dirname in os.listdir(pathcompany):
	full_company_names.append(dirname)

for fname in os.listdir(path):
	file = open(path + fname, 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = fname.replace('_cleaned.tsv', '')
	foo = foo.replace('&', '')
	foo = foo.replace(' ', '')
	exec (foo + '_stockdata' + " = arr")

for name in full_company_names:
	name = name.replace(' ', '').replace('&', '').replace('_', '')
	varname = name + "_stockdata"
	exec("stockarr = " + varname)
	for row in stockarr[1:]:
		stockdata_dict[name + '_' + row[1]] = row[8]

##########################################################
############## open files containing words ###############
##########################################################

good_words = open("Vocab/good_words.txt", "r")
bad_words =  open("Vocab/bad_words.txt", "r")

#good_clusters = open("Vocab_Clusters/goodwords_clustered.txt", "r")
#bad_clusters = open("Vocab_Clusters/badwords_clustered.txt", "r")


###########################################################
#append all the words and their contexts to various arrays#
###########################################################
good_arr = []
bad_arr = []

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


##########################################################################################
###                         loop through all the companies                             ### 
##########################################################################################
count = 0
#for cluster in good_clusters_arr:
#	count+=1
#for cluster in bad_clusters_arr:
#	count+=1
#cluster_count = count


for company_name in full_company_names:

	datecount = 0
	outfarr = []

	correlated_words = open(company_name + "newsfinalwords.txt", "r")
	correlated_arr = []
	good_correlated_arr = []
	bad_correlated_arr = []

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

	outf = open('./newsdescriptors/' + company_name + '_descriptor.tsv', 'w')
	outfarr = []
	outfarr.append([])
	outfarr[0].append('DATE')
	outfarr[0].append('COMPANY')
	outf.write('DATE' + '\t' + 'COMPANY' + '\t') 
	for word in good_correlated_arr:
		outf.write(word + "\t")
	for word in bad_correlated_arr:
		outf.write(word + "\t")
	outf.write('STOCK VALUE' + "\t")
	#for i in range(0, cluster_count):
	#	outf.write("Cluster_" + str(i+1) + "\t")
	outf.write('\n')

	for filename in os.listdir('../News/ArticlesData/' + company_name):
		filename = filename.replace('&', '').replace(' ', '')
		date = filename.split('_')[-2]

		outf.write(str(date) + "\t" + str(company_name) + "\t")

		corpusReader = nltk.corpus.PlaintextCorpusReader('../News/ArticlesData/'+ company_name, filename)
		articlelinecount = len(corpusReader.sents())

		for word in good_correlated_arr:
			allvalues[str(company_name) + "_" + str(word)] = 0
		for word in bad_correlated_arr:
			allvalues[str(company_name) + "_" + str(word)] = 0


		for sentence in corpusReader.sents():
			for word in sentence:
				if word.lower() in good_correlated_arr:
					allvalues[str(company_name) + "_" + str(word.lower())] += 1
				elif word.lower() in bad_correlated_arr:
					allvalues[str(company_name) + "_" + str(word.lower())] += 1

		for x in allvalues:
			allvalues[x] = allvalues[x]/articlelinecount
				

######################################################################################################
################                      GENERATING DESCRIPTORS                       ###################
######################################################################################################
		DESCRIPTOR = []
		for word in good_correlated_arr:
			DESCRIPTOR.append(allvalues[company_name + "_" + word])
		for word in bad_correlated_arr:
			DESCRIPTOR.append(allvalues[company_name + "_" + word])
		try:
			DESCRIPTOR.append(stockdata_dict[company_name.replace(' ', '').replace('&', '').replace('_', '') + '_' + date])
		except KeyError:
			DESCRIPTOR.append('N/A (weekend)')
	
		for value in DESCRIPTOR:
			outf.write(str(value) + '\t')
		outf.write('\n')
