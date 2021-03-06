from __future__ import division
import csv
import os 
from scipy import stats
import numpy as np

######################################################
############## READING GOOD/BAD WORDS ################
######################################################

good_words = open("Vocab/good_words.txt", "r")
bad_words =  open("Vocab/bad_words.txt", "r")
good_arr = []
bad_arr = []

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

##############################################################
################ READING GOOD/BAD SYNONYMS ###################
##############################################################

goodsynfile = open("synonyms/good_synonyms.csv", "r")
badsynfile = open("synonyms/bad_synonyms.csv", "r")
reader = csv.reader(goodsynfile, delimiter=',')
goodsynarr = list(reader)
reader = csv.reader(badsynfile, delimiter=',')
badsynarr = list(reader)

synonyms_dict = {}

for row in goodsynarr:
        if len(row) != 0:
                synonyms_dict[row[0]] = []
                synonyms = row[1].split('_')
                for synonym in synonyms:
                	if synonym != '':
                		synonyms_dict[row[0]].append(synonym)
for row in badsynarr:
        if len(row) != 0:
                synonyms_dict[row[0]] = []
                synonyms = row[1].split('_')
                for synonym in synonyms:
                	if synonym != '':
                		synonyms_dict[row[0]].append(synonym)


##################################################################
######################## READING DATASETS ########################
##################################################################

path = '../stock_data/tweet_date_data/'
namespath = '../News/ArticlesData/'
full_company_names = []

for dirname in os.listdir(namespath):
	full_company_names.append(dirname)
print(full_company_names)

for fname in os.listdir(path):
	file = open(path + fname, 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = fname.replace('_cleaned.tsv', '').replace('&', '').replace(' ', '').replace('_','')
	exec (foo + '_stockdata' + " = arr")

path2 = 'newsfrequencies/'
for name in full_company_names:
	file = open('newsfrequencies/' + name + '_wordfrequencies.tsv', 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = name.replace(' ', '').replace('&', '').replace('_','')
	exec(foo + '_wordfreq' + " = arr")

allwords = Apple_wordfreq[0][2:]

stockdata_dict = {}
wordfreq_dict = {}

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
			wordfreq_dict[name + '_' + freqarr[0][i] + '_' + row[0]] = float(row[i])

##############################################################
################### CLUSTER PROCESSING #######################
##############################################################
clusters_dict = {}
for name in full_company_names:

	for filename in os.listdir('../AllTweets/filteredTweets/' + name):
		date = filename.split('_')[1].replace('Tweets.txt', '')

		for word in synonyms_dict:

			count = 0

			try:
				clusters_dict[name + '_' + word + '_' + date] = wordfreq_dict[name + '_' + word + '_' + date]
			except KeyError:
				clusters_dict[name + '_' + word + '_' + date] = 0

			for synonym in synonyms_dict[word]:
				try:
					clusters_dict[name + "_" + word + "_" + date] += wordfreq_dict[name + "_" + synonym + "_" + date]
					count += 1
				except KeyError:
					continue

			if count != 0:
				clusters_dict[name + '_' + word + '_' + date] /= count
			print(clusters_dict[name + '_' + word + '_' + date])
print('DONE WITH CLUSTERS!!!')



company_dict = {}

for name in full_company_names:
	name = name.replace(' ', '').replace('&', '').replace('_', '')
	company_dict[name] = {}
	for word in allwords:
		company_dict[name][word] = [[],[]]

for entity in clusters_dict:
	entity = entity.split('_')
	company_name = entity[0]
	word = entity[1]
	date = entity[2]
	try:
		if stockdata_dict[company_name + '_' + date] == '+':
			company_dict[company_name][word][1].append(1)
		elif stockdata_dict[company_name + '_' + date] == '-':
			company_dict[company_name][word][1].append(0)
		elif stockdata_dict[company_name + '_' + date] == '=':
			company_dict[company_name][word][1].append(0)
		company_dict[company_name][word][0].append(float(wordfreq_dict[company_name + '_' + word + '_' + date]))
	except KeyError:
		continue

# sum = 0
# for num in (company_dict['Apple']['win'][0]):
# 	sum += num
# print('number of time win appears', sum)

finalwords = []
for name in full_company_names:
	outfcompany = open('newsfinalwords/' + name + 'newsfinalwords.txt', 'w')
	name = name.replace(' ', '').replace('&', '').replace('_','')
	for word in company_dict[name]:
		if len(company_dict[name][word][0]) > 0:
			a = np.array(company_dict[name][word][0])
			b = np.array(company_dict[name][word][1])
			if stats.pointbiserialr(a,b)[0] > 0.30 or stats.pointbiserialr(a,b)[0] < -.30:
				finalwords.append(word)
				outfcompany.write(word + '\n')

				#print(name)
				#print(word, stats.pointbiserialr(a,b)[0], stats.pointbiserialr(a,b)[1])
				#print(company_dict[name][word])
