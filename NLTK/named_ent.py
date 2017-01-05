import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords,state_union
from nltk.stem import PorterStemmer



ps=PorterStemmer()
example_text = "Hello there, how are you doing today? The weather is great and Python is awesome. The sky is pinkish blue. You should not eat cardboard."
example_sentence= "This is an example showing off stop word filtration."
example_words=["python","pythoner","pythoning","pythoned","pythonly"]
new_text = "It is very important to be pythonly while you are pythoning with python. All pythoners have pythoned poorly at least once."
words = word_tokenize(new_text)
train_text= state_union.raw("2005-GWBush.txt")
sample_text= state_union.raw("2006-GWBush.txt")



custom_sent_tokenizer= PunktSentenceTokenizer(train_text)

tokenized= custom_sent_tokenizer.tokenize(sample_text)

def process_content():
	for i in tokenized:
		words=nltk.word_tokenize(i)
		tagged = nltk.pos_tag(words)
		named_Ent=nltk.ne_chunk(tagged)
		named_Ent.draw()



process_content()
