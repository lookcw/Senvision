from PyDictionary import PyDictionary
import BeautifulSoup
import os
import sys
import csv

vocab_folder="../CorrelationAnalysis/Vocab/"
all_synonyms_folder="../CorrelationAnalysis/synonyms/"
dictionary=PyDictionary()
print (dictionary.synonym("best-dictionary","xml"))

# def is_ascii(s):
#     return all(ord(c) < 128 for c in s)

# def writeSyns(word):
# 	towrite=[]
# 	syns=[]
# 	dict= (dictionary.synonym(word,"lxml"))
# 	if dict:
# 		for x in dict:
# 			towrite.append(x.rstrip("\n"))
# 			for syn in dict[x]:
# 				if is_ascii(syn):
# 					syns.append(syn)
# 		stringsyns="_".join(syns)
# 		towrite.append(stringsyns)
# 		return towrite
# 	return towrite



# for subdir, dirs, files in os.walk(vocab_folder):
#     for file in files:
# 	vocab_file=vocab_folder+file
# 	all_synonyms_file=all_synonyms_folder+	 file[0:file.find("_")+1]+"synonyms.csv"
# 	output=open(all_synonyms_file,'w')	
# 	csvwriter=csv.writer(output,delimiter=",")
# 	vocab=open(vocab_file,"r")
# 	with vocab as f:
# 	    for line in f:
# 	    	print line,
# 	        csvwriter.writerow(writeSyns(line))

