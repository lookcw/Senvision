import json
import urllib2  # the lib that handles the url stuff
import os
import subprocess

data = urllib2.urlopen("https://api.stocktwits.com/api/2/streams/symbol/AAPL.json")
print data

company_tickers=["AAPL","INTC","WMT","BA","MRK","JPM","PG","GOOGL"]

json_str = subprocess.call(["curl", "-X","GET", "https://api.stocktwits.com/api/2/streams/symbol/AAPL.json"])	
#url=urllib2.urlopen("https://api.stocktwits.com/api/2/streams/symbol/AAPL.json")
#print url
#result = json.loads("https://api.stocktwits.com/api/2/streams/symbol/AAPL.json")  # result is now a dict
#print result
d = json.loads(str(json_str))

print d



