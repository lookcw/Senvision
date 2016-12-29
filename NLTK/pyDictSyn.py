from PyDictionary import PyDictionary
import BeautifulSoup
import os
import sys
import csv

vocab_folder="../CorrelationAnalysis/Vocab/"
all_synonyms_folder="../CorrelationAnalysis/synonyms/"
dictionary=PyDictionary()

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def writeSyns(word):
	towrite=[]
	syns=""
	dict= (dictionary.synonym(word,"lxml"))
	if dict:
		for x in dict:
			towrite.append(x.rstrip("\n"))
			for syn in dict[x]:
				if is_ascii(syn):
					syns+= str(syn) + "_"
		towrite.append(syns)
		return towrite
	return towrite



for subdir, dirs, files in os.walk(vocab_folder):
    for file in files:
	vocab_file=vocab_folder+file
	all_synonyms_file=all_synonyms_folder+	 file[0:file.find("_")+1]+"_synonyms.csv"
	output=open(all_synonyms_file,'w')
	csvwriter=csv.writer(output,delimiter=",")
	vocab=open(vocab_file,"r")
	with vocab as f:
	    for line in f:
	    	print line,
	    	print writeSyns(line)
	        csvwriter.writerow(writeSyns(line))

