from __future__ import division
import csv
import os 
from scipy import stats
import numpy as np
#stats.pointbiserialr(x,y)
#returns correlation coefficient and p-value

path = '../stock_data/tweet_date_data/'
full_company_names = []

for fname in os.listdir(path):
	full_company_names.append(fname.replace('_cleaned.tsv', ''))

#full_company_names.remove('Walmart')
#full_company_names.remove('p&g')

for fname in os.listdir(path):
	file = open(path + fname, 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = fname.replace('_cleaned.tsv', '')
	foo = foo.replace('&', '')
	foo = foo.replace(' ', '')
	exec (foo + '_stockdata' + " = arr")

path2 = 'newsfrequencies/'
for name in full_company_names:
	file = open('newsfrequencies/' + name + '_wordfrequencies.tsv', 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = name.replace(' ', '')
	foo = foo.replace('&', '')
	exec(foo + '_wordfreq' + " = arr")

allwords = Google_wordfreq[0][2:]

# path3 = 'tweetcounts/'
# for name in full_company_names:
# 	file = open('tweetcounts/' + name + '_tweetcounts.tsv', 'r')
# 	reader = csv.reader(file, delimiter='\t')
# 	arr = list(reader)
# 	foo = name.replace(' ', '').replace('&', '')
# 	exec(foo + '_tweetcounts' + " = arr")

stockdata_dict = {}
wordfreq_dict = {}
#tweetcounts_dict = {}

for name in full_company_names:
	name = name.replace(' ', '')
	name = name.replace('&', '')
	varname = name + "_stockdata"
	exec("stockarr = " + varname)
	for row in stockarr[1:]:
		stockdata_dict[name + '_' + row[1]] = row[8]

# for name in full_company_names:
#         name = name.replace(' ', '')
#         name = name.replace('&', '')
# 	varname = name + "_tweetcounts"
# 	exec ("countarr = " + varname)
# 	for row in countarr[1:]:
# 		tweetcounts_dict[name + '_' + row[0]] = int(row[2])

#print(tweetcounts_dict)

for name in full_company_names:
	name = name.replace(' ', '')
	name = name.replace('&', '')
	varname = name + "_wordfreq"
	exec("freqarr = " + varname)
	for row in freqarr[1:]:
		#print(row)
		for i in range(2, len(row)-1):
			#print('company name', name)
			#print('word', freqarr[0][i])
			#print('date', row[0])
			#print('value', row[i])
			#print(tweetcounts_dict[name + '_' + row[0]], 'tweet counts')
			#print(row[i], 'raw frequency')
			wordfreq_dict[name + '_' + freqarr[0][i] + '_' + row[0]] = float(row[i])
			#if name == "Apple" and freqarr[0][i] == "loses":
			#	print(int(row[i]), 1000 * (int(row[i])/(tweetcounts_dict[name + '_' + row[0]])))
			#if (int(row[i])) > 0:
					#print(name, int(row[i]), 1000 * (int(row[i])/(tweetcounts_dict[name + '_' + row[0]])), freqarr[0][i], row[0])

#print(wordfreq_dict)

for x in wordfreq_dict:
	dictkey = x.split('_')
	comp_name = dictkey[0]
	word = dictkey[1]
	date = dictkey[2]
	#if comp_name == 'Apple' and word == 'loses':
		#print(wordfreq_dict[x])


company_dict = {}

for name in full_company_names:
	name = name.replace(' ', '').replace('&', '')
	company_dict[name] = {}
	for word in allwords:
		company_dict[name][word] = [[],[]]


#print(company_dict.keys())

for entity in wordfreq_dict:
	entity = entity.split('_')
	company_name = entity[0]
	word = entity[1]
	date = entity[2]
	try:
		#print('STOCK DIRECTION', stockdata_dict[company_name + '_' + date])
		#print('WORD FREQUENCY', wordfreq_dict[company_name + '_' + word + '_' + date])
		if stockdata_dict[company_name + '_' + date] == '+':
			company_dict[company_name][word][1].append(1)
		elif stockdata_dict[company_name + '_' + date] == '-':
			company_dict[company_name][word][1].append(0)
		elif stockdata_dict[company_name + '_' + date] == '=':
			company_dict[company_name][word][1].append(0)
		#company_dict[company_name][word][1].append(stockdata_dict[company_name + '_' + date])
		company_dict[company_name][word][0].append(float(wordfreq_dict[company_name + '_' + word + '_' + date]))
	except KeyError:
		continue

sum = 0
for num in (company_dict['Apple']['win'][0]):
	sum += num
print('number of time win appears', sum)

#print(company_dict['Apple']['loses'])
finalwords = []
outf = open('newsfinalwords.txt', 'w')
for name in full_company_names:
	name = name.replace(' ', '').replace('&', '')
	for word in company_dict[name]:
		if len(company_dict[name][word][0]) > 0:
			a = np.array(company_dict[name][word][0])
			b = np.array(company_dict[name][word][1])
			if stats.pointbiserialr(a,b)[0] > 0.30 or stats.pointbiserialr(a,b)[0] < -.30:
			#if 1 == 1:
				#print(company_dict[name][word])
				print(word, stats.pointbiserialr(a,b)[0], stats.pointbiserialr(a,b)[1])
				finalwords.append(word)
				outf.write(word + '\n')
