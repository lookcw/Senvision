from eventregistry import *
er = EventRegistry()
q = QueryArticles()

def getArticlesUrls(queryterm,date):

	#set the date limit of interest
	q.setDateLimit(datetime.date(2014, 4, 16), datetime.date(2014, 4, 28))
	# find articles mentioning the company Apple		
	q.addConcept(er.getConceptUri("Apple"))
	# return the list of top 30 articles, including the concepts, categories and article image
	q.addRequestedResult(RequestArticlesUrlList(page=1,count=30))
	writefile=open(queryterm+"_"+date+"_Urls.txt",'w')
	
	results=str(er.execQuery(q))
	writefile.write(results)
	writefile.close()


getArticlesUrls("Apple","2014-4-16")
