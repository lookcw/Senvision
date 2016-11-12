from eventregistry import *
er = EventRegistry()
q = QueryArticles()
# set the date limit of interest
q.setDateLimit(datetime.date(2014, 4, 16), datetime.date(2014, 4, 28))
# find articles mentioning the company Apple
q.addConcept(er.getConceptUri("Apple"))
# return the list of top 30 articles, including the concepts, categories and article image
q.addRequestedResult(RequestArticlesInfo(page = 1, count = 30, 
    returnInfo = ReturnInfo(articleInfo = ArticleInfoFlags(concepts = True, categories = True, image = True))))
res = er.execQuery(q)
