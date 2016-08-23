import csv
arr = []

#noticed: closing price != opening price next day
company = raw_input("enter company name: ")

f = open('./alldata/' + str(company)+ ".csv", "r")
reader = csv.reader(f, delimiter=",")
for row in reader:
	arr.append(row)

#print(arr[0])
# col 1 is open and col 4 is close

#separate headings of array from its data
headings = arr[0]
headings.append("+/-")
headings.append("% change")
arr.remove(arr[0])

#strip down to first few dates
newarr = arr[0:10]
for row in newarr:
	if float(row[1]) > float(row[4]):
		row.append('-')
	elif float(row[1]) < float(row[4]):
		row.append('+')
	elif float(row[1]) == float(row[4]):
		row.append('no change')

	pcent_change = ( (float(row[4]) - float(row[1])) / float(row[1]) ) * 100
	row.append(pcent_change)

outf = open('./cleaned_data/' + str(company) + ".csv", "w")

for x in headings:
	outf.write(str(x) + "\t")
outf.write("\n")
for row in newarr:
	for x in row:
		outf.write(str(x) + "\t")
	outf.write("\n")
