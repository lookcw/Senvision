import csv
import random
import datetime

ticker_names=["INTC","ETE","ETFC","NDAQ"]
results_file=open("Future_predictions.csv",'w')
randomized_writer=csv.writer(results_file,delimiter=',')
now = datetime.datetime.now()
randomized_writer.writerow(["Date","Symbol","pred"])
for i in ticker_names:
        k=random.random()
        if k>.5:
                randomized_writer.writerow([now.date(),i,"+"])
        else:
                randomized_writer.writerow([now.date(),i,"-"])
