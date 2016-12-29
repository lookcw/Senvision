from __future__ import division
import os
import csv
from datetime import date, timedelta as td
import nltk
import logging
import argparse
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

allvalues = {}

##########################################################
# argument parsing
##########################################################
parser = argparse.ArgumentParser()
parser.add_argument("company", help="company to run program for", type=int)
args = parser.parse_args()
company_running = args.company
print(company_running)

##########################################################
# open files containing words ############################
##########################################################

good_words = open("Vocab/good_words.txt", "r")
bad_words =  open("Vocab/bad_words.txt", "r")

###########################################################
#append all the words and their contexts to various arrays#
###########################################################
good_arr = []
bad_arr = []

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


######################################################################################################
###                            COMPANY_NAMES AND DATE COLLECTION                                   ###
######################################################################################################
full_company_names = []
for name in os.listdir("../News/ArticlesData/"):
	full_company_names.append(name)
full_company_names = [full_company_names[company_running]]
print(full_company_names)

for company_name in full_company_names:
        for word in good_arr:
                allvalues[str(company_name) + "_" + str(word)] = 0
        for word in bad_arr:
                allvalues[str(company_name) + "_" + str(word)] = 0

#print (allvalues)

##########################################################################################
###                         loop through all the companies                             ### 
##########################################################################################
for company_name in full_company_names:
#if 1 == 2:
	if company_name == 'JPMorgan_Chase':
		company_string = 'J.P. Morgan'
	elif company_name == 'Procter_&_Gamble':
		company_string = 'Procter'
	elif company_name == 'INTC':
		company_string = 'Intel'
	else:
		company_string = company_name


	outf = open('./newsfrequencies/' + company_name + '_wordfrequencies.tsv', 'w')
	outf.write('DATE' + '\t' + 'COMPANY' + '\t')
	for word in good_arr:
		outf.write(str(word) + "\t")
	for word in bad_arr:
		outf.write(str(word) + "\t")
	outf.write('\n')


	for filename in os.listdir('../News/ArticlesData/' + company_name):

		date = filename.split('_')[1]

		outf.write(str(date) + "\t" + str(company_name) + "\t")

		file1 = open('../News/ArticlesData/' + company_name + '/'  + filename, 'rU')
		#reader = csv.reader(file1, dialect=csv.excel_tab)
		corpusReader = nltk.corpus.PlaintextCorpusReader('../News/ArticlesData/'+ company_name, filename)
		articlelinecount = len(corpusReader.sents())

		for sentence in corpusReader.sents():
			for word in sentence:
				if word.lower() in good_arr or word.lower() in bad_arr:
					allvalues[str(company_name) + "_" + str(word.lower())] += 1

                
######################################################################################################
################                      GENERATING DESCRIPTORS                       ###################
######################################################################################################

		DESCRIPTOR_FREQUENCY = []

		for word in good_arr:
			DESCRIPTOR_FREQUENCY.append(allvalues[str(company_name) + "_" + str(word.lower())]/articlelinecount)
		for word in bad_arr:
			DESCRIPTOR_FREQUENCY.append(allvalues[str(company_name) + "_" + str(word.lower())]/articlelinecount)

		for value in DESCRIPTOR_FREQUENCY:
			outf.write(str(value) + '\t')
		outf.write('\n')

		for value in allvalues:
			allvalues[value] = 0	
