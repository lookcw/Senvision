import pandas as pd
import os
import quandl
import time

auth_tok = "sJ1-JesK6dU83RFsYBkF"

data = quandl.get("WIKI/KO", trim_start = "2000-12-12", trim_end = "2014-12-30", authtoken=auth_tok)
data2 = quandl.get("WIKI/INTC", trim_start = "2016-12-12", trim_end = "2017-3-30", authtoken=auth_tok)
print data2

print type(data)