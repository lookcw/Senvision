import csv
import os 
from scipy import stats
#stats.pointbiserialr(x,y)
#returns correlation coefficient and p-value

path = '/Users/smadan/Documents/Bitbucket/stock_data/tweet_date_data/'
full_company_names = []

for fname in os.listdir(path):
	full_company_names.append(fname.replace('_cleaned.tsv', ''))
print(full_company_names)

for fname in os.listdir(path):
	file = open(path + fname, 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = fname.replace('_cleaned.tsv', '')
	foo = foo.replace('&', '')
	foo = foo.replace(' ', '_')
	exec (foo + '_stockdata' + " = arr")

path2 = 'frequencies/'
for name in full_company_names:
	file = open('frequencies/' + name + '_wordfrequencies.tsv', 'r')
	reader = csv.reader(file, delimiter='\t')
	arr = list(reader)
	foo = name.replace(' ', '_')
	foo = foo.replace('&', '')
	print(foo)
	exec(foo + '_wordfreq' + " = arr")

allwords = Apple_wordfreq[0][2:]


stockdata_dict = {}
freq_dict = {}

for name in full_company_names:
	varname = name + '_stockdata[1:]'
	exec("for row in " + varname + ":")
		stock_datadict[name + '_' + row[1]] = row[8]

print stock_datadict
