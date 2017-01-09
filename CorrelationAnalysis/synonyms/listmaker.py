import csv

goodfile = open("good_synonyms.csv", "r")
badfile = open("bad_synonyms.csv", "r")
outfile = open("all_words.csv", "w")

reader = csv.reader(goodfile, delimiter=',')
goodsynarr = list(reader)
reader = csv.reader(badfile, delimiter=',')
badsynarr = list(reader)

allwordsarr = []
synonyms_dict = {}

for row in goodsynarr:
	if len(row) != 0:
		synonyms_dict[row[0]] = []
		if row[0] not in allwordsarr:
			allwordsarr.append(row[0])
		synonyms = row[1].split('_')
		for synonym in synonyms:
			if synonym != '':
				synonyms_dict[row[0]].append(synonym)
			if synonym not in allwordsarr:
				allwordsarr.append(synonym)

for row in badsynarr:
        if len(row) != 0:
		synonyms_dict[row[0]] = []
                if row[0] not in allwordsarr:
                        allwordsarr.append([row[0]])
                synonyms = row[1].split('_')
                for synonym in synonyms:
			if synonym != '':
				synonyms_dict[row[0]].append(synonym)
                        if synonym not in allwordsarr:
                                allwordsarr.append(synonym)

print(synonyms_dict['zippy'])

for word in allwordsarr:
	if word == '':
		allwordsarr.remove(word)

writer = csv.writer(outfile, delimiter="\n")
writer.writerow(allwordsarr)
