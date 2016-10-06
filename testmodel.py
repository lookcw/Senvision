import os
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#company_name = raw_input("Enter company name: ")


class MySentences(object):
	def __init__ (self,dirname):
		self.dirname = dirname
	def __iter__ (self):
		for fname in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname,fname)):
				yield line.split()


#COMPANY_NAMES:
full_company_names = ['Apple', 'Boeing', 'Google', 'Intel', 'Merck', 'Morgan Chase', 'p&g', 'Walmart']
#company_name = raw_input("Enter company name: ")
dates = []
current_year = "2016"
current_month = "09"
firstdate = raw_input("Enter start date (put a 0 on front if single digit): ")
lastdate = raw_input("Enter end date: ")
for i in range (int(firstdate), int(lastdate)+1):
	if len(str(i)) == 1:
		dates.append(str(current_year) + "-" + str(current_month) + "-0" + str(i))
	else:
		dates.append(str(current_year) + "-" + str(current_month) + "-" + str(i))



#WORDS
positive_words = ['good', 'great', 'success', 'successful', 'succeed', 'achieve', 'achievement', 'achieved', 'innovate', 'competitive', 'gain', 'up', 'rise', 'acquire', 'win']
neutral_words = ['revenue', 'profit', 'performance']
negative_words = ['bad', 'worse', 'worst', 'failure', 'obsolete', 'cut', 'horrible', 'struggle', 'struggling', 'bankrupt', 'loss', 'down', 'fail', 'lose', 
'suit', 'lawsuit', 'sue', 'court', 'lawyer', 'controversy']



for company_name in full_company_names:

	outf = open('./descriptors/' + str(company_name) + "_descriptor" + ".txt", 'w')

	outf.write('Word' + "\t")
	for x in positive_words:
		outf.write(str(x) + "\t")
	for y in negative_words:
		outf.write(str(y) + "\t")
	outf.write("\n")

	for date in dates:

		outf.write(str(date) + "\t")

		num_features = 40 #subject to change
		min_word_count = 1 #subject to change
		num_workers = 15 #should be good
		context = 10 #subject to change
		#downsampling = 1e-3

		sentences = LineSentence('/Users/smadan/Documents/Bitbucket/tweetanalysis/replacedTweets/' + company_name + '/'  + company_name + '_' + date + 'Tweets.txt')
		print("Training model...")
		model = word2vec.Word2Vec(sentences, workers=num_workers, size=num_features, min_count=min_word_count, window=context)

		posarr = []
		negarr = []

		for x in positive_words:
			try:
				dist = model.similarity(str(company_name), x)
				posarr.append(dist)
			except KeyError:
				posarr.append('N/A')
				continue
 
		for x in negative_words:
			try:
				dist = model.similarity(str(company_name), x) 
				negarr.append(dist) 
			except KeyError:
				negarr.append('N/A')
				continue

#		print(posarr)
#		print(negarr)

#		neutral_pos = ['good', 'great', 'rise', 'up', 'win', 'raise', 'increase', 'gain']
#		neutral_neg = ['cut', 'horrible', 'low', 'lower', 'lose', 'loss', 'fall', 'bankrupt', 'failure', 'terrible', 'decrease', 'loss']


#		outf.write('MOST SIMILAR WORDS' + '\n')
#		simarr = model.most_similar(str(company_name))
#		for x in simarr:
#			try:
#				for y in x:
#					outf.write(str(y) + '\t')
#				outf.write('\n')
#			except UnicodeEncodeError:
#				continue

		for distance in posarr:
			outf.write(str(distance) + '\t')
		for distance in negarr:
			outf.write(str(distance) + '\t')
		outf.write('\n')
