from __future__ import division
import csv
import os 
from scipy import stats
import numpy as np

path = '../stock_data/tweet_date_data/'
namespath = '../News/ArticlesData/'
full_company_names = []

for dirname in os.listdir(namespath):
	full_company_names.append(dirname)

for fname in os.listdir(path):
	file = open(path + fname, 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = fname.replace('_cleaned.tsv', '')
	foo = foo.replace('&', '').replace(' ', '').replace('_','')
	exec (foo + '_stockdata' + " = arr")

path2 = 'newsfrequencies/'
for name in full_company_names:
	file = open('newsfrequencies/' + name + '_wordfrequencies.tsv', 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = name.replace(' ', '').replace('&', '').replace('_','')
	exec(foo + '_wordfreq' + " = arr")

allwords = Google_wordfreq[0][2:]

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


for x in wordfreq_dict:
	dictkey = x.split('_')
	comp_name = dictkey[0]
	word = dictkey[1]
	date = dictkey[2]


company_dict = {}

for name in full_company_names:
	name = name.replace(' ', '').replace('&', '').replace('_', '')
	company_dict[name] = {}
	for word in allwords:
		company_dict[name][word] = [[],[]]


for entity in wordfreq_dict:
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

sum = 0
for num in (company_dict['Apple']['win'][0]):
	sum += num
print('number of time win appears', sum)

finalwords = []
outf = open('newsfinalwords.txt', 'w')
full_company_names.remove("Walmart")
for name in full_company_names:
	outfcompany = open(name + 'newsfinalwords.txt', 'w')
	name = name.replace(' ', '').replace('&', '').replace('_','')
	for word in company_dict[name]:
		if len(company_dict[name][word][0]) > 0:
			a = np.array(company_dict[name][word][0])
			b = np.array(company_dict[name][word][1])
			if stats.pointbiserialr(a,b)[0] > 0.30 or stats.pointbiserialr(a,b)[0] < -.30:
				print(name)
				print(word, stats.pointbiserialr(a,b)[0], stats.pointbiserialr(a,b)[1])
				print(company_dict[name][word])
				finalwords.append(word)
				outf.write(word + '\n')
				outfcompany.write(word + '\n')
