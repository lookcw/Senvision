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
full_company_names = []
for name in os.listdir("../AllTweets/filteredTweets/"):
	full_company_names.append(name)
full_company_names = [company_running]

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

	outf = open('./frequencies/' + company_name + '_wordfrequencies.tsv', 'w')
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
		date = filename.split('_')[1]

		outfarr[datecount].append(date)
		outfarr[datecount].append(company_name)

		file1 = open('../AllTweets/filteredTweets/' + company_name + '/'  + filename, 'rU')
		corpusReader = nltk.corpus.PlaintextCorpusReader('../AllTweets/filteredTweets/'+ company_name, filename)	
		tweetcount = len(corpusReader.sents())

		for sentence in corpusReader.sents():
			for word in sentence:
				# if word.lower() in good_arr or word.lower() in bad_arr:
				if word.lower() in syn_arr:
					allvalues[str(company_name) + "_" + str(word.lower())] += 1
                
######################################################################################################
################                      GENERATING DESCRIPTORS                       ###################
######################################################################################################
		DESCRIPTOR_FREQUENCY = []

		#for word in good_arr:
		for word in syn_arr:
			DESCRIPTOR_FREQUENCY.append(allvalues[str(company_name) + "_" + str(word.lower())]/articlelinecount)
		# for word in bad_arr:
		# 	DESCRIPTOR_FREQUENCY.append(allvalues[str(company_name) + "_" + str(word.lower())]/articlelinecount)

		for value in DESCRIPTOR_FREQUENCY:
			outfarr[datecount].append(str(value))

		for value in allvalues:
			allvalues[value] = 0	
	
	writer = csv.writer(outf, delimiter='\t')
	for row in outfarr:
		writer.writerow(row)
