import codecs
import os
import time
from eventregistry import *
from datetime import date, timedelta as td

CompanyNames=["Merck","Procter & Gamble","Walmart","Boeing","JPMorgan Chase","Google","INTC","Apple"]

def comp_to_folder_name(comp):
	if comp=="INTC":
		return "Intel"
	elif comp=="JPMorgan Chase":
		return "JPMorganChase"
	elif comp=="Procter & Gamble":
		return "Procter&Gamble" 
	else:
		return comp	



print "must be run inside the folder \"News/Fetcher\""


def getArticlesUrls(queryterm,startdate,enddate):
	folder_name=comp_to_folder_name(queryterm)
	companyfolderpath="../Urls/"+folder_name
	writefilepath=companyfolderpath+"/"+folder_name+"_"+str(startdate)+"_Urls.txt"
	if(os.path.isfile(writefilepath)): #checks if file exists. If it does, exit function
		print "skipping "+ folder_name+ " "+str(startdate)
		return
	print "running " +queryterm+ " " +str(startdate)
	er = EventRegistry()
	q = QueryArticles(lang=["eng"],isDuplicateFilter="skipDuplicates",hasDuplicateFilter="skipHasDuplicates")
	if not os.path.exists(companyfolderpath): #checks if folder exists. If not, make it
		os.makedirs(companyfolderpath)
		print "created" + companyfolderpath
	#set the date limit of interest
	q.setDateLimit(startdate, enddate)
	# find articles mentioning the company Apple		
	q.addConcept(er.getConceptUri(queryterm))
	# return the list of top 30 articles, including the concepts, categories and article image
	q.addRequestedResult(RequestArticlesUrlList(page=1,count=150))
	writefile=open(companyfolderpath+"/"+queryterm+"_"+str(startdate)+"_Urls.txt",'w')
	results=er.execQuery(q)
	print results
	if('urlList' not in results.keys()):
		print "exiting because urlLists not in keys"
		sys.exit(0)
	if  (len(results['urlList']['results'])!=0):
		#print str(results)
		diction=results
		for url in diction['urlList']['results']:
			writefile.write(url.encode('utf-8') + "\n") #writes url by line to file
		print("# of Urls: " + str(len(diction['urlList']['results'])))
		writefile.close()
		time.sleep(1)
	else:
		sys.exit(0)
		


def iterateDays(startyear,startmonth,startdate,endyear,endmonth,enddate):#runs getArticlesUrls over range of dates
	print datetime.datetime.now()

	d1 = date(startyear, startmonth, startdate)
	d2 = date(endyear, endmonth, enddate)

	delta = d2 - d1
	
	for i in range(delta.days + 1):
		currentDate= d1 + td(days=i)
		nextDate=d1+td(days=i+1)
		for company in CompanyNames:
			print company
			if getArticlesUrls(company,currentDate,nextDate)==3:
				return
			
now= datetime.datetime.now()
now-td(days=1)

iterateDays(2016,12,15,now.year,now.month,now.day)
		 
#getArticlesUrls("Apple",date(2016,9,15),date(2016,9,16))	
