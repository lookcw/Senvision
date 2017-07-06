import json
import urllib  # the lib that handles the url stuff
import os
import datetime
import time

#data = urllib2.urlopen("https://api.stocktwits.com/api/2/streams/symbol/AAPL.json")
#print type(data)

#retrieves data from json file and saves it to files in the stocktwits folder. The folders are named by their ticker name
#The file names are in the format of Date_Companyname_"twits.txt"
company_tickers=["AAPL","INTC","WMT","BA","MRK","JPM","PG","GOOGL"]
time_run = datetime.datetime.now()
now = datetime.datetime.now()

while (time_run.date()==now.date()):
	for i in company_tickers:
		url = "https://api.stocktwits.com/api/2/streams/symbol/"+i+".json"
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		now = datetime.datetime.now()
		print now.date()
		if not os.path.exists("stocktwits/"+i):
	    		os.makedirs("stocktwits/"+i)
		tweetfile=open("stocktwits/"+i+"/"+str(now.date())+"_"+i+"_"+"twits.txt",'a')
		for key in data["messages"]:
			print key["body"]
			string=key["body"].encode('utf-8').strip()
			tweetfile.write(string+"\n")
	time.sleep(60*6)
