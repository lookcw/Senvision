*Java files that deal with stock data fetching, tweet data retrieving with a lagtime of 2 days, converting streamed URLs to news articles, and generating vocab clusters.
*Basically just misc tasks that we used Java for.
*must be run inside Senvision Folder, not Jars folder.
*Data Pairer puts the dates of the news that will be taken to predict that date on. For example, for 2017-3-15, it will put in 2017-3-12 as the news date to predict on 2017-315
*TweetDataRetriever uses the twitter streaming api to get Tweets from the past 9 days, You only get a certain amount of queries every 15 minutes. They are put into filtered Tweets. The correct month version exists because some computers have a weird problem with the current date, and think java wants to query the previous month, so I made it so it pulls the month one ahead. Correct month is the one that has the current month coded in
*UrlsToArticleConverter.jar turns the URLS from the News Pulling program into articles in News/ArticlesData

