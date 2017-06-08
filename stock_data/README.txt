*Here we pull and process financial data.
*quandlpull.py pulls financial data from Quandl (we may use Google Finance in the future).
*the pulled data from quandlpull.py goes into "alldata".
*stocktable.py calculates movement of stock prices from day to day and puts them into cleaned_data.
*dates for Tweets corresponding to the stock movement are then matched in tweet_date_data.
