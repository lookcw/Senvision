from timeout import timeout
import codecs
import os
import time
from eventregistry import *
from datetime import date, timedelta as td
import multiprocessing







global currentKey
currentKey="f3472b56-284f-4c86-9312-c08eeafaa579"
#apiKey="f3472b56-284f-4c86-9312-c08eeafaa579"
q = QueryArticles(lang=["eng"],isDuplicateFilter="skipDuplicates",hasDuplicateFilter="skipHasDuplicates")

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

def runResults(er):
	print "in runResults"
	return er.execQuery(q)

def getArticlesUrls(queryterm,startdate,enddate):
	folder_name=comp_to_folder_name(queryterm)
	companyfolderpath="../Urls/"+folder_name
	writefilepath=companyfolderpath+"/"+folder_name+"_"+str(startdate)+"_Urls.txt"
	if(os.path.isfile(writefilepath)): #checks if file exists. If it does, exit function
		print "skipping "+ folder_name+ " "+str(startdate)
		return
	#print "running " +queryterm+ " " +str(startdate)
	
	apiKey1="f3472b56-284f-4c86-9312-c08eeafaa579"
	apiKey2="ac7cc08e-279d-42a0-b8b8-09abfaf145ff"
	global currentKey
	print currentKey
	er = EventRegistry(apiKey=currentKey)
	#set the date limit of interest
	q.setDateLimit(startdate, enddate)
	# find articles mentioning the company Apple		
	q.addConcept(er.getConceptUri(queryterm))
	print "after adding conepts"
	# return the list of top 30 articles, including the concepts, categories and article image
	q.addRequestedResult(RequestArticlesUrlList(page=1,count=150))
	
        if not os.path.exists(companyfolderpath): #checks if folder exists. If not, make it
      		os.makedirs(companyfolderpath)
		print "created" + companyfolderpath
	
	writefile=open(companyfolderpath+"/"+folder_name+"_"+str(startdate)+"_Urls.txt",'w')
	print "right before query"
	p = multiprocessing.Process(target=runResults(er))
	p.start()
	print "why is this absolute garbage"
	# Wait for 10 seconds or until process finishes
	p.join(1)

	# If thread is still active
	if p.is_alive():
        	print "running... let's kill it..."
	
        	# Terminate
        	p.terminate()
       		p.join()
		if currentKey==apiKey1:
			currentKey=apiKey2
			return
		else:
			sys.exit(0)
	try:
		print "trying to run"
		print "ran results"
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
	except:
		print "failed"
def iterateDays(startyear,startmonth,startdate,endyear,endmonth,enddate):#runs getArticlesUrls over range of date)
	d1 = date(startyear, startmonth, startdate)
	d2 = date(endyear, endmonth, enddate)

	

	delta = d2 - d1
	
	for i in range(delta.days + 1):
		currentDate= d1 + td(days=i)
		nextDate=d1+td(days=i+1)
		for company in CompanyNames:
	#		print company
			if getArticlesUrls(company,currentDate,nextDate)==3:
				return
			
now= datetime.datetime.now()
now-=td(days=1)

iterateDays(2017,5,26,now.year,now.month,now.day)
		 
#getArticlesUrls("Apple",date(2016,9,15),date(2016,9,16))	
