import pandas as pd
import os
import quandl
import time

auth_tok = "sJ1-JesK6dU83RFsYBkF"

#position of Tickername and company name must always be the same, dictionary of names made from these two arrays
TickerNames=["INTC","AAPL","BA","GOOGL","JPM","MRK","PG","WMT"]
CompNames=["Intel","Apple","Boeing","Google","JPMorganChase","Merck","Procter&Gamble","Walmart"]


ticker2Comp={}
for i in range(len(TickerNames)):
	ticker2Comp[TickerNames[i]]=CompNames[i]


#Pulls data from Quandl
for i in TickerNames:
	print time.strftime("%d-%m-%Y")
	data_intel = quandl.get("WIKI/"+str(i),trim_start = "2016-07-01", trim_end = time.strftime("%d-%m-%Y"), authtoken=auth_tok)
	f = open("alldata/" + ticker2Comp[i] + ".csv", "w")
	data_intel.to_csv("alldata/"+str(ticker2Comp[i])+'.csv', header=True, index=True, sep=',')


import csv
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

