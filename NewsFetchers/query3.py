
from eventregistry import *
import time

er = EventRegistry()
recentQ = GetRecentArticles(maxArticleCount = 200)
while True:
    articleList = recentQ.getUpdates(er)
    print "%d articles were added since the last call" % len(articleList)

    # do whatever you need to with the articles in articleList        

    # wait a while before asking for new articles
    time.sleep(20)     
