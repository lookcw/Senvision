from __future__ import division
import os
import csv
import nltk
from datetime import date, timedelta as td
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stockdata_dict = {}
wordfreq_dict = {}

namespath = '../AllTweets/filteredTweets/'
full_company_names = []
for dirname in os.listdir(namespath):
	full_company_names.append(dirname)
print(full_company_names)

path = '../stock_data/tweet_date_data/'
for fname in os.listdir(path):
	file = open(path + fname, 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = fname.replace('_cleaned.tsv', '').replace('&', '').replace(' ', '').replace('_', '')
	exec (foo + '_stockdata' + " = arr")

path2 = 'tweetclusterfrequencies/'
for name in full_company_names:
	file = open(path2 + name + '_clusterfrequencies.tsv', 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = name.replace(' ', '').replace('&', '').replace('_','')
	exec(foo + '_wordfreq' + " = arr")

for name in full_company_names:
	name = name.replace(' ', '').replace('&', '').replace('_', '')
	varname = name + "_stockdata"
	exec("stockarr = " + varname)
	for row in stockarr[1:]:
		stockdata_dict[name + '_' + row[1]] = row[8]

for name in full_company_names:
	name = name.replace(' ', '').replace('&', '').replace('_', '')
	varname = name + "_wordfreq"
	exec("freqarr = " + varname)
	for row in freqarr[1:]:
		for i in range(2, len(row)-1):
			wordfreq_dict[name + '_' + freqarr[0][i].replace('_cluster', '') + '_' + row[0]] = float(row[i])

##########################################################
############## open files containing words ###############
##########################################################

good_words = open("Vocab/good_words.txt", "r")
bad_words =  open("Vocab/bad_words.txt", "r")


###########################################################
#append all the words and their contexts to various arrays#
###########################################################
good_arr = []
bad_arr = []


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



for company_name in full_company_names:

	correlated_words = open('tweetfinalwords/' + company_name + "tweetsfinalwords.txt", "r")
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

	outf = open('./tweetdescriptors/' + company_name + '_descriptor.tsv', 'w')
	outf.write('DATE' + '\t' + 'COMPANY' + '\t') 
	for word in correlated_arr:
		outf.write(word + "\t")
	outf.write("PRICE DIRECTION")
	outf.write('\n')

	for filename in os.listdir('../AllTweets/filteredTweets/' + company_name):

		date = filename.split('_')[1].replace('Tweets.txt', '').replace('Tweets+.txt', '')

		if str(company_name + '_' + date) in stockdata_dict.keys():
			outf.write(str(date) + "\t" + str(company_name) + "\t")
			for word in correlated_arr:
				try:
					outf.write(str(wordfreq_dict[company_name + '_' + word + '_' + date]) + '\t')
				except KeyError:
					outf.write(str(0) + '\t')
			outf.write(str(stockdata_dict[company_name + '_' + date]))
			outf.write('\n')

		else:
			continue
			

# ######################################################################################################
# ################                      GENERATING DESCRIPTORS                       ###################
# ######################################################################################################
# 		DESCRIPTOR = []
# 		for word in good_correlated_arr:
# 			DESCRIPTOR.append(allvalues[company_name + "_" + word])
# 		for word in bad_correlated_arr:
# 			DESCRIPTOR.append(allvalues[company_name + "_" + word])
	
# 	for value in DESCRIPTOR:
# 		outf.write(str(value) + '\t')
# 	outf.write('\n')
