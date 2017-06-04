import codecs
import os
import time
from eventregistry import *
from datetime import date, timedelta as td

CompanyNames=["Merck","Procter & Gamble","Walmart","Boeing","JPMorgan Chase","Google","Intel","Apple"]

print "must be run inside the folder \"NewsFetcher\""


def getArticlesUrls(queryterm,startdate,enddate):
	er = EventRegistry()
	q = QueryArticles(lang=["eng"],isDuplicateFilter="skipDuplicates",hasDuplicateFilter="skipHasDuplicates")
	#set the date limit of interest
	q.setDateLimit(startdate, enddate)
	# find articles mentioning the company Apple		
	q.addConcept(er.getConceptUri(queryterm))
	# return the list of top 30 articles, including the concepts, categories and article image
	q.addRequestedResult(RequestArticlesInfo(page = 1, count = 30, 
    returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(concepts = True))))
	print er.execQuery(q)



def iterateDays(startyear,startmonth,startdate,endyear,endmonth,enddate):#runs getArticlesUrls over range of dates


	d1 = date(startyear, startmonth, startdate)
	d2 = date(endyear, endmonth, enddate)

	delta = d2 - d1
	
	for i in range(delta.days + 1):
		currentDate= d1 + td(days=i)
		nextDate=d1+td(days=i+1)
		for company in CompanyNames:
			getArticlesUrls(company,currentDate,nextDate)
			
now= datetime.datetime.now()

#iterateDays(2016,10,5,now.year,now.month,now.day)
iterateDays(2016,11,13,now.year,now.month,now.day)
		 
#getArticlesUrls("Apple",date(2016,9,15),date(2016,9,16))	
