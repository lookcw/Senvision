import os
import csv
from datetime import date, timedelta as td
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

allvalues = {}

#company_name = raw_input("Enter company name: ")

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
#full_company_names = ['Google', 'Intel', 'Merck', 'Morgan Chase', 'p&g', 'Walmart']
#full_company_names = ['Apple']
dates = []


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
#	outf = open('./frequencies/' + company_name + '_wordfrequencies.tsv', 'w')
	outf = open('./tweetcounts/' + company_name + '_tweetcounts.tsv', 'w')
	outf.write('DATE' + '\t' + 'COMPANY' + '\t') 
#	for word in good_arr:
#		outf.write(str(word) + "\t")
#	for word in bad_arr:
#		outf.write(str(word) + "\t")
	outf.write('TWEET COUNT')
	outf.write('\n')

	for filename in os.listdir('../AllTweets/filteredTweets/' + company_name):
		index1 = filename.index('_')
		index2 = filename.index('T')
		date = filename[index1+1:index2]

		outf.write(str(date) + "\t" + str(company_name) + "\t")

		#sentences = LineSentence('../AllTweets/filteredTweets/' + company_name + '/'  + filename)
		file1 = open('../AllTweets/filteredTweets/' + company_name + '/'  + filename, 'rU')
		reader = csv.reader(file1, dialect=csv.excel_tab)
		tweetcount = len(list(reader))
		
		posarr = []
		negarr = []

		#for sentence in sentences:
		#	for word in sentence:
		#		if word.lower() in good_arr or word.lower() in bad_arr:
		#			allvalues[str(company_name) + "_" + str(word.lower())] += 1
		#print(allvalues["Apple_loses"])
                
######################################################################################################
################                      GENERATING DESCRIPTORS                       ###################
######################################################################################################
		DESCRIPTOR = []
		#for word in good_arr:
		#	DESCRIPTOR.append(allvalues[str(company_name) + "_" + str(word.lower())])
		#for word in bad_arr:
		#	DESCRIPTOR.append(allvalues[str(company_name) + "_" + str(word.lower())])

		#for value in DESCRIPTOR:
		#	outf.write(str(value) + '\t')
		#outf.write('\n')
		outf.write(str(tweetcount) + '\n')
		#for value in allvalues:
		#	allvalues[value] = 0	
