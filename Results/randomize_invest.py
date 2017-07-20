import csv
import random
import datetime
from datetime import timedelta
ticker_names=["INTC","ETE","ETFC","NDAQ"]
results_file=open("Future_predictions.csv",'w')
randomized_writer=csv.writer(results_file,delimiter=',')
now = datetime.datetime.now()
print now.hour
print now.minute
if now.hour == 16 and now.minute >30 or now.hour > 16:
	now = now + timedelta(days=1)
randomized_writer.writerow(["date","symbol","pred"])
for i in ticker_names:
        k=random.random()
        if k>.5:
                randomized_writer.writerow([now.date(),i,"+"])
        else:
                randomized_writer.writerow([now.date(),i,"-"])
