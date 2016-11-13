import codecs
import os
from eventregistry import *
from datetime import date, timedelta as td

CompanyNames=["Merck","Procter & Gamble","Walmart","Boeing","JPMorgan Chase","Google","Intel","Apple"]

print "must be run inside the folder \"NewsFetcher\""


def getArticlesUrls(queryterm,startdate,enddate):
	companyfolderpath="../NewsUrls/"+queryterm
	writefilepath=companyfolderpath+"/"+queryterm+"_"+str(startdate)+"_Urls.txt"
	if(os.path.isfile(writefilepath)): #checks if file exists. If it does, exit function
		print "skipping "+ queryterm+ " "+str(startdate)
		return
	print "running " +company+ " " +str(currentDate)
	er = EventRegistry()
	q = QueryArticles(lang=["eng"],isDuplicateFilter="skipDuplicates")
	if not os.path.exists(companyfolderpath): #checks if folder exists. If not, make it
		os.makedirs(companyfolderpath)
		print "created" + companyfolderpath
	#set the date limit of interest
	q.setDateLimit(startdate, enddate)
	# find articles mentioning the company Apple		
	q.addConcept(er.getConceptUri(queryterm))
	# return the list of top 30 articles, including the concepts, categories and article image
	q.addRequestedResult(RequestArticlesUrlList(page=1,count=100))
	writefile=open(companyfolderpath+"/"+queryterm+"_"+str(startdate)+"_Urls.txt",'w')	
	results=er.execQuery(q)
	#print str(results)
	dict=results
	for url in dict['urlList']['results']: 
		writefile.write(url.encode('utf-8') + "\n") #writes url by line to file
	print("# of Urls: "+ len(dict['urlList']['results']))
	writefile.close()



def iterateDays(startyear,startmonth,startdate,endyear,endmonth,enddate):


	d1 = date(startyear, startmonth, startdate)
	d2 = date(endyear, endmonth, enddate)

	delta = d2 - d1
	
	for i in range(delta.days + 1):
		currentDate= d1 + td(days=i)
		nextDate=d1+td(days=i+1)
		for company in CompanyNames:
			getArticlesUrls(company,currentDate,nextDate)
			
iterateDays(2016,10,5,2016,10,9)
		 
#getArticlesUrls("Apple",date(2016,9,15),date(2016,9,16))	
