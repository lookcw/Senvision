import csv
import os
import codecs

#noticed: closing price != opening price next day
#companies = ['apple', 'boeing', 'google', 'intel', 'merck', 'jpm', 'walmart', 'pandg']

for filename in os.listdir("./auto_pulled_data"):
	arr = []
	f = open('./auto_pulled_data/' + str(filename), "r")
	try:
		reader = csv.reader(f, delimiter=",")
		for row in reader:
			arr.append(row)
	except csv.Error:
		continue

	#print(arr[0])
	#col 1 is open and col 4 is close
	#separate headings of array from its data

	headings = arr[0]
	headings.append("+/-")
	headings.append("% change")
	arr.remove(arr[0])

	#strip down to first few dates
	for row in arr:
		if float(row[7]) > float(row[4]):
			row.append('-')
		elif float(row[7]) < float(row[4]):
			row.append('+')
		elif float(row[7]) == float(row[4]):
			row.append('-')

		pcent_change = ( (float(row[4]) - float(row[1])) / float(row[1]) ) * 100
		row.append(pcent_change)

	outf = open('./cleaned_data/' + str(filename).replace(".csv","") + "_cleaned.csv", "w")

	for x in headings:
		outf.write(str(x) + "\t")
	outf.write("\n")
	for row in arr:
		for x in row:
			outf.write(str(x) + "\t")
		outf.write("\n")
