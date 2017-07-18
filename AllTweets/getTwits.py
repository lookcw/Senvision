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
		read_tweetfile=open("stocktwits/"+i+"/"+str(time_run.date())+"_"+i+"_"+"twits.txt",'r')
		all_tweets = read_tweetfile.readlines()
		read_tweetfile.close()
		tweetfile=open("stocktwits/"+i+"/"+str(now.date())+"_"+i+"_"+"twits.txt",'a')
		for i in range(len(all_tweets)):
			all_tweets[i]=all_tweets[i].strip()
		print "number of tweets alrady in file:_________________________________________" ,len(all_tweets)
		try:
			for key in data["messages"]:
				#print key["body"]
				tweet=key["body"].encode('utf-8').strip()
				#print all_tweets
				if tweet not in all_tweets:
					print tweet
					tweetfile.write(tweet+"\r\n")
			print "done streaming"
		except:
			print "key error"
			time.sleep(60*50)
		tweetfile.close()

	time.sleep(60*15)

	
