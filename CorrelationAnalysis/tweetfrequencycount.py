from __future__ import division
import nltk
import argparse
import os
import csv
from datetime import date, timedelta as td
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

allvalues = {}

##########################################################
# argument parsing
##########################################################
parser = argparse.ArgumentParser()
#parser.add_argument("company", help="company to run program for", type=int)
parser.add_argument("company", type=str)
args = parser.parse_args()
company_running = args.company
print(company_running)

full_company_names = []
for name in os.listdir("../AllTweets/filteredTweets/"):
	full_company_names.append(name)
full_company_names = [company_running]


##########################################################
# open files containing words ############################
##########################################################

good_words = open("Vocab/good_words.txt", "r")
bad_words =  open("Vocab/bad_words.txt", "r")
synonyms = open("synonyms/all_words.csv", "r")

###########################################################
#append all the words and their contexts to various arrays#
###########################################################
good_arr = []
bad_arr = []
syn_arr = []

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

reader = csv.reader(synonyms, delimiter = " ")
for row in reader:
	for item in row:
		syn_arr.append(item)
for word in syn_arr:
        if word == '':
                syn_arr.remove(word) 

######################################################################################################
###                            COMPANY_NAMES AND DATE COLLECTION                                   ###
######################################################################################################
for company_name in full_company_names:
        # for word in good_arr:
        #         allvalues[str(company_name) + "_" + str(word)] = 0
        # for word in bad_arr:
        #         allvalues[str(company_name) + "_" + str(word)] = 0
        for word in syn_arr:
        	allvalues[str(company_name) + "_" + str(word)] = 0	


##########################################################################################
###                         loop through all the companies                             ### 
##########################################################################################
for company_name in full_company_names:
#if 1 == 2:
	outfarr = []
	datecount = 0

	outf = open('./tweetfrequencies/' + company_name + '_wordfrequencies.tsv', 'w')
	outfarr.append([])
	outfarr[0].append('DATE')
	outfarr[0].append('COMPANY')
	# for word in good_arr:
	# 	outfarr[0].append(word)
	# for word in bad_arr:
	# 	outfarr[0].append(word)
	for word in syn_arr:
		outfarr[0].append(word)


	for filename in os.listdir('../AllTweets/filteredTweets/' + company_name):

		datecount+=1
		outfarr.append([])
		filename = filename.replace('+', '\+')
		date = filename.split('_')[1].replace('Tweets.txt', '').replace('Tweets+.txt', '')
		#print(date)
		#print(filename)

		outfarr[datecount].append(date)
		outfarr[datecount].append(company_name)

		corpusReader = nltk.corpus.PlaintextCorpusReader('../AllTweets/filteredTweets/'+ company_name, filename)
		tweetcount = len(corpusReader.sents())

		all_words = []
		for w in corpusReader.words():
			all_words.append(w.lower())
		all_words = nltk.FreqDist(all_words)
		#print(all_words.most_common(15))
		#print(all_words["stupid"])

		for word in syn_arr:
			try:
				allvalues[str(company_name) + "_" + str(word.lower())] = all_words[word.lower()]
			except KeyError:
				allvalues[str(company_name) + "_" + str(word.lower())] = 0

                
######################################################################################################
################                      GENERATING DESCRIPTORS                       ###################
######################################################################################################
		DESCRIPTOR_FREQUENCY = []

		#for word in good_arr:
		for word in syn_arr:
			DESCRIPTOR_FREQUENCY.append(allvalues[str(company_name) + "_" + str(word.lower())]/tweetcount)
		# for word in bad_arr:
		# 	DESCRIPTOR_FREQUENCY.append(allvalues[str(company_name) + "_" + str(word.lower())]/tweetcount)

		for value in DESCRIPTOR_FREQUENCY:
			outfarr[datecount].append(str(value))

		#print(allvalues['Boeing_hinder'])

		for value in allvalues:
			allvalues[value] = 0	
	
	writer = csv.writer(outf, delimiter='\t')
	for row in outfarr:
		writer.writerow(row)

