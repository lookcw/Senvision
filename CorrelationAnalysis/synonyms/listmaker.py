import csv

goodfile = open("good_synonyms.csv", "r")
badfile = open("bad_synonyms.csv", "r")
outfile = open("all_words.csv", "w")

reader = csv.reader(goodfile, delimiter=',')
goodsynarr = list(reader)[:-1]
reader = csv.reader(badfile, delimiter=',')
badsynarr = list(reader)[:-1]

allwordsarr = []


for row in goodsynarr:
	if len(row) != 0:
		if [row[0]] not in allwordsarr:
			allwordsarr.append([row[0]])
		synonyms = row[1].split('_')
		for synonym in synonyms:
			if [synonym] not in allwordsarr:
				allwordsarr.append([synonym])

for row in badsynarr:
        if len(row) != 0:
                if [row[0]] not in allwordsarr:
                        allwordsarr.append([row[0]])
                synonyms = row[1].split('_')
                for synonym in synonyms:
                        if [synonym] not in allwordsarr:
                                allwordsarr.append([synonym])

print(allwordsarr)

writer = csv.writer(outfile, delimiter="\n")
for row in allwordsarr:
	writer.writerow(row)
