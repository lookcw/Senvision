import os
from gensim.models import word2vec
from gensim.models.word2vec import LineSentence
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

company_name = raw_input("Enter company name: ")

class MySentences(object):
	def __init__ (self,dirname):
		self.dirname = dirname
	def __iter__ (self):
		for fname in os.listdir(self.dirname):
			for line in open(os.path.join(self.dirname,fname)):
				yield line.split()

num_features = 40
min_word_count = 1
num_workers = 15
context = 10
#downsampling = 1e-3
sentences = MySentences('Intel_8_13')
print("Training model...")
model = word2vec.Word2Vec(sentences, workers=num_workers, size=num_features, min_count=min_word_count, window=context)

outf = open(str(company_name) + '_8_13_word_similarities.txt', 'w')

posarr = []
negarr = []

positive_words = ['good', 'great', 'success', 'successful', 'succeed', 'achieve', 'achievement', 'achieved', 'innovate', 'competitive', 'gain', 'up', 'rise', 'acquire', 'win']
neutral_words = ['revenue', 'profit', 'performance']
negative_words = ['bad', 'worse', 'worst', 'failure', 'obsolete', 'cut', 'horrible', 'struggle', 'struggling', 'bankrupt', 'loss', 'down', 'fail', 'lose']

cont = raw_input('Do you want to find the similarity b/w two words? ')
while cont == 'yes':
	x = raw_input('Enter a word you want to find similarity of: ')
	y = raw_input('Enter second word: ')
	try: 
		print(model.similarity(x, y))
	except KeyError:
		print('Sorry, no tweets for >= 1 of those words.')

	cont = raw_input('Do you want to find the similarity b/w two words? ')

outf.write('POSITIVE DISTANCES' + "\n")
for x in positive_words:
	try:
		dist = model.similarity(str(company_name), x)
		posarr.append(dist)
		outf.write(str(company_name) + "\t"  + str(x) + "\t" + str(dist))
		outf.write("\n")
	except KeyError:
		posarr.append('0')
		continue

outf.write('NEGATIVE DISTANCES' + "\n") 
for x in negative_words:
	try:
        	dist = model.similarity(str(company_name), x) 
		negarr.append(dist)
        	outf.write(str(company_name) + "\t"  + str(x) + "\t" + str(dist))
        	outf.write("\n") 
	except KeyError:
		negarr.append('N/A')
		continue


print(posarr)
print(negarr)

neutral_pos = ['good', 'great', 'rise', 'up', 'win', 'raise', 'increase', 'gain']
neutral_neg = ['cut', 'horrible', 'low', 'lower', 'lose', 'loss', 'fall', 'bankrupt', 'failure', 'terrible', 'decrease', 'loss']


outf.write('MOST SIMILAR WORDS' + "\n")
simarr = model.most_similar(str(company_name))
for x in simarr:
	try:
		for y in x:
			outf.write(str(y) + "\t")
		outf.write("\n")
	except UnicodeEncodeError:
		continue

descriptors = open('descriptors_8_13.txt', 'w')

for word in positive_words:
	descriptors.write(word + "\t")
descriptors.write('\n')
for num in posarr:
        descriptors.write(num + "\t") 
descriptors.write('\n')

for word in negative_words:
        descriptors.write(word + "\t") 
descriptors.write('\n') 
for num in negarr:
        descriptors.write(num + "\t")
