import pandas as pd
import os
import quandl
import time

auth_tok = "sJ1-JesK6dU83RFsYBkF"

#print (type(data))
data_intel = quandl.get("WIKI/INTC", trim_start = "2016-07-01", trim_end = "2017-3-30", authtoken=auth_tok)
data_intel.to_csv('intel.csv', header=True, index=True, sep=',')

data_apple = quandl.get("WIKI/AAPL", trim_start = "2016-07-01", trim_end = "2017-3-30", authtoken=auth_tok)
data_apple.to_csv('apple.csv', header=True, index=True, sep=",")

data_boeing = quandl.get("WIKI/BA", trim_start = "2016-07-01", trim_end = "2017-3-30", authtoken=auth_tok)
data_boeing.to_csv('boeing.csv', header=True, index=True, sep=",")

data_google = quandl.get("WIKI/GOOGL", trim_start = "2016-07-01", trim_end = "2017-3-30", authtoken=auth_tok)
data_google.to_csv('google.csv', header=True, index=True, sep=",")

data_jpmorganchase = quandl.get("WIKI/JPM", trim_start = "2016-07-01", trim_end = "2017-3-30", authtoken=auth_tok)
data_jpmorganchase.to_csv('jpm.csv', header=True, index=True, sep=",")

data_merck = quandl.get("WIKI/MRK", trim_start = "2016-07-01", trim_end = "2017-3-30", authtoken=auth_tok)
data_merck.to_csv('merck.csv', header=True, index=True, sep=",")

data_png = quandl.get("WIKI/PG", trim_start = "2016-07-01", trim_end = "2017-3-30", authtoken=auth_tok)
data_png.to_csv('png.csv', header=True, index=True, sep=",")

data_walmart = quandl.get("WIKI/WMT", trim_start = "2016-07-01", trim_end = "2017-3-30", authtoken=auth_tok)
data_walmart.to_csv('walmart.csv', header=True, index=True, sep=",")

