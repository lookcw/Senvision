#creates descriptors based on NER
import nltk 
# from nltk.corpus import state_union
# sample = state_union.raw("2006-GWBush.txt")
import codecs
import os
import unicodecsv as csv

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

article_dir = '../News/ArticlesData'
twitter_dir = '../AllTweets/filteredTweets'

num_common_words=1000                                                                                                                  
subdirs = [x[0] for x in os.walk(twitter_dir)]                                                                            
for subdir in subdirs:     
	print subdir
	entity_names = []
	files = os.walk(subdir).next()[2]# 	
	if (len(files) > 0):
		for file in files:
			filename=subdir + "/" + file
			with codecs.open(filename, 'r',encoding='latin-1') as f:
				sample = f.read()
			sentences = nltk.sent_tokenize(sample)
			tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
			tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
			chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
			for tree in chunked_sentences:
			    entity_names.extend(extract_entity_names(tree))
	all_NER = nltk.FreqDist(entity_names)
	NER_features = [x[0] for x in all_NER.most_common(num_common_words)]
	write_file=open("News_Common_NER/"+subdir.split("/")[-1]+"_top_"+str(num_common_words)+"_words.tsv",'w')
	writer=csv.writer(write_file,delimiter='\t')
	writer.writerow(NER_features)


def find_features_comp(subdir):
	print subdir
	comp=subdir.split("/")[-1]
	files = os.walk(subdir).next()[2]
	#######opening files per comp
	stock_file=open("../stock_data/tweet_date_data/"+comp+"_cleaned.tsv",'r')
	stock_reader=csv.reader(stock_file,delimiter='\t')
	common_words=open("News_Common_NER/"+comp+"_top_"+str(num_common_words)+"_words.tsv",'r')
	word_reader=csv.reader(common_words,delimiter='\t')
	descriptor_file=open("news_NER_descriptors/"+comp+"_descriptor.tsv",'w')
	descriptor_writer=csv.writer(descriptor_file,delimiter='\t')
	word_features=next(word_reader)
	stock_lines=list(stock_reader)
	stock_dict={}
	descriptors=[]
	for line in stock_lines:
		stock_dict[line[1]]=line[-2]
	if (len(files) > 0): 
		for file in files:
			print file
			entity_names=[]
			filec = file.replace('+', '\+')
			filename=subdir + "/" + file
			with codecs.open(filename, 'r',encoding='latin-1') as f:
				sample = f.read()
			sentences = nltk.sent_tokenize(sample)
			tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
			tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
			chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
			for tree in chunked_sentences:
			    entity_names.extend(extract_entity_names(tree))     
			date = file.split('_')[1]
			features = {}
			for w in word_features:
				k=w in entity_names
				features[w]=k
				#features[w] = (all_words[w])
			if date in stock_dict:
				descriptors.append([date,features,stock_dict[date]])
				descriptor_writer.writerow([date,stocklinefeatures,stock_dict[date]])

# for subdir in subdirs[1:]:
# 	find_features_comp(subdir)
# # Print all entity names
# print entity_names

# Print unique entity names