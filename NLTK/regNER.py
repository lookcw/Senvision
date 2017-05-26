#creates descriptors based on NER of either news or tweets. These 
#descriptors are in the form of a csv where the first column 
#is the date and the second is a dictionary of whether the NER exists or not.
import nltk 
# from nltk.corpus import state_union
# sample = state_union.raw("2006-GWBush.txt")
import codecs
import os
import unicodecsv as csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')





#accepting data_type and whether need to find most common word arguments.
n=1
for argument in sys.argv[1:]:
  if (argument == "-type"):
    data_type= sys.argv[n+1]
  if argument == "-com":
    com = sys.argv[n+1] 
  n+=1
if ((data_type!="tweet" and data_type!="news") or (com!="y" and com!="n")):
	print "Set -type to 'tweet' or 'news' and com to 'y' or 'n' depending on if you want to recalculate common words."

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

output=''
if data_type=="tweet":
	data_dir='../AllTweets/filteredTweets' #the tweet data
	common_words_file="Tweet_Common_NER" #the tweet common words from the above 
	output="twitter_NER_descriptors" #the folder the desciptors will be put into.
if data_type=="news":
	data_dir='../News/ArticlesData'
	common_words_file="News_Common_NER"
	output="news_NER_descriptors_2_days"

#find x most common NERx
num_common_words=1000                                                                                                                  
subdirs = [x[0] for x in os.walk(data_dir)]

entity_names=[]
#calculate common words
if(com=='y'):
	for subdir in subdirs[1:]:#actions per company
		print "calculating common NER",subdir
		entity_names = []
		files = os.walk(subdir).next()[2]#extracts file names and puts them in an array
		if (len(files) > 0):
			for file in files:
				filename=subdir + "/" + file
				print filename
				with codecs.open(filename, 'r','latin-1') as f:
					sample = f.read()
				sentences = nltk.sent_tokenize(sample)
				print "past sentences"
				tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
				tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
				print "whyy"
				chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
				for tree in chunked_sentences:
					entity_names.extend(extract_entity_names(tree))
				filename=subdir + "/" + file
				print filename
		all_NER = nltk.FreqDist(entity_names)
		NER_features = [x[0] for x in all_NER.most_common(num_common_words)]
		write_file=open(common_words_file+"/"+subdir.split("/")[-1]+"_top_"+str(num_common_words)+"_words.tsv",'w')
		writer=csv.writer(write_file,delimiter='\t')
		writer.writerow(NER_features)

#descriptor writer per file,
def find_features_comp(subdir):
	print subdir
	comp=subdir.split("/")[-1]
	files = os.walk(subdir).next()[2]

	#######opening files per comp
	stock_file=open("../stock_data/tweet_date_data/"+comp+"_cleaned.tsv",'r')
	stock_reader=csv.reader(stock_file,delimiter='\t')
	common_words=open(common_words_file+"/"+comp+"_top_"+str(num_common_words)+"_words.tsv",'r')
	word_reader=csv.reader(common_words,delimiter='\t')
	dates_done=[]

	#If com is yes, then write all new descriptors, otherwise just append.
	if(com=="y"):
		descriptor_file=open(output+"/"+comp+"_descriptor.tsv",'w')
	else:
		descriptor_file=open(output+"/"+comp+"_descriptor.tsv",'a')
		descriptor_file_read=open(output+"/"+comp+"_descriptor.tsv",'r')
		descriptor_reader=csv.reader(descriptor_file_read,delimiter='\t')
		descriptor_lines=list(descriptor_reader)
		for line in descriptor_lines:
			dates_done.append(line[0])
	descriptor_writer=csv.writer(descriptor_file,delimiter='\t')


	word_features=next(word_reader) #the common words 
	stock_lines=list(stock_reader)
	stock_dict={}
	descriptors=[]

	#set key of date equal to value of +/-
	for line in stock_lines:
		stock_dict[line[1]]=line[-2]

	print stock_dict
	#create descriptors and add value to end
	if (len(files) > 0): 
		for file in files:
			#print file
			entity_names=[]
			filec = file.replace('+', '\+')
			if(data_type=="tweet"):
				date = file.split('_')[1].split("Tweet")[0]
			if(data_type=="news"):
				date = file.split('_')[1]
			filename=subdir + "/" + file
			#print "reached before if statement"
			if date not in dates_done and com!="y" and date in stock_dict:
				print "Running NLTK"
				with codecs.open(filename, 'r','latin-1') as f:
					sample = f.read()
				#start nltk analysis
				sentences = nltk.sent_tokenize(sample)
				tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
				tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
				chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
				for tree in chunked_sentences:
				    entity_names.extend(extract_entity_names(tree))
				print date
				features = {}
				for w in word_features:
					k=w in entity_names
					features[w]=k
				#write nltk results
				if date in stock_dict:
					descriptors.append([date,features,stock_dict[date]])
					descriptor_writer.writerow([date,features,stock_dict[date]])


for subdir in subdirs[1:]:
	print subdir
	find_features_comp(subdir)
# Print all entity names
print entity_names

# Print unique entity names 
