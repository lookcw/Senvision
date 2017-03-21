import csv
import random

results_file=open("NLTK_predictions.csv",'r')
results_reader=csv.reader(results_file,delimiter=',')
randomized_file=open("randomized_predictions.csv",'w')
randomized_writer = csv.writer(randomized_file,delimiter=',')
for line in results_reader:
	k=random.random()
	if k>.5:
		randomized_writer.writerow([line[0],line[1],"+"])
	else:
		randomized_writer.writerow([line[0],line[1],"-"])
