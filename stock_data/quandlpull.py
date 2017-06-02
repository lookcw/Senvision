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
	data_intel = quandl.get("WIKI/"+str(i),trim_start = "2016-07-01", trim_end = time.strftime("%d-%m-%Y"), authtoken=auth_tok)
	f = open("alldata/" + ticker2Comp[i] + ".csv", "w")
	data_intel.to_csv("alldata/"+str(ticker2Comp[i])+'.csv', header=True, index=True, sep=',')
