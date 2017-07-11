import tweepy
import json
import datetime
import os
import time
auth = tweepy.OAuthHandler("GkNo1eVzDrIvx4WX0UF2IQvUy",  "u44NuHRf7zWJS3oXNCMruJnDyUqugAKTYReSAV5cykHkQ3vxp5")
auth.set_access_token("763207677463920640-cTCEshVK13VFegFjrUry1p5tyUa98Ux", "xx5fQbbIjv6zzGv7FrzUXdqxmpOe0tyO8s48zNApMG84y")

api = tweepy.API(auth)

#retrieves data from json file and saves it to files in the stocktweets folder. The folders are named by their ticker name
#The file names are in the format of Date_Companyname_"tweets.txt"
company_tickers=["AAPL","INTC","WMT","BA","MRK","JPM","PG","GOOGL"]
time_run = datetime.datetime.now()
now = datetime.datetime.now()

while (time_run.date()==now.date()):
	for i in company_tickers:
		query = "$"+i
		max_tweets = 100
		if not os.path.exists("stocktweets/"+i):
			os.makedirs("stocktweets/"+i)
		tweetfile=open("stocktweets/"+i+"/"+str(now.date())+"_"+i+"_"+"tweets1.txt",'a')
		read_tweetfile=open("stocktweets/"+i+"/"+str(now.date())+"_"+i+"_"+"tweets1.txt",'rb')
		now = datetime.datetime.now()
		print now.date()
		all_tweets = read_tweetfile.readlines()
		for i in all_tweets:
			print i
		print "==============================end of all Tweets=========================="
		#print all_tweets
		print "number of tweets alrady in file:_________________________________________" ,len(all_tweets)
		searched_tweets = [status for status in tweepy.Cursor(api.search, q=query,lang="en").items(max_tweets)]	
		try:
			for i in range(len(searched_tweets)):
				json_str = json.dumps(searched_tweets[i]._json)
				data = json.loads(json_str)
				tweet=data["text"].encode('utf-8').strip()+"\r\n"
				if tweet not in all_tweets:
						print "adding tweet"				
						tweetfile.write(tweet)
				else:
					print "ignoring tweet"
			print "==========================end of new tweets==========================="
		except tweepy.TweepError:
			print "Rate used up"
			time.sleep(60*50)
		read_tweetfile.close()
		tweetfile.close()
	time.sleep(60*15)
