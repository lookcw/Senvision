import csv
import os
import codecs

#noticed: closing price != opening price next day
#companies = ['apple', 'boeing', 'google', 'intel', 'merck', 'jpm', 'walmart', 'pandg']

for filename in os.listdir("./alldata"):
	arr = []
	f = open('./alldata/' + str(filename), "r")
	try:
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			arr.append(row)
	except csv.Error:
		continue

	#print(arr[0])
	#col 9 is open and col 12 is close
	#separate headings of array from its data

	headings = arr[0]
	headings.append("+/-")
	headings.append("% change")
	arr.remove(arr[0])

	#strip down to first few dates
	for row in arr:
		if float(row[11]) > float(row[8]):
			row.append('+')
		elif float(row[11]) < float(row[8]):
			row.append('-')
		elif float(row[11]) == float(row[8]):
			row.append('-')
		pcent_change = ( (float(row[11]) - float(row[8])) / float(row[8]) ) * 100
		row.append(pcent_change)

	outf = open('./cleaned_data/' + str(filename).replace(".csv","") + "_cleaned.csv", "w")

	for x in headings:
		outf.write(str(x) + "\t")
	outf.write("\n")
	for row in arr:
		for x in row:
			outf.write(str(x) + "\t")
		outf.write("\n")
