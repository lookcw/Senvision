import newspaper



cnn_paper = newspaper.build('http://www.pcauthority.com.au/Review/454462,review-android-wear-20.aspx')
for article in cnn_paper.articles:
    print(article.url)

for category in cnn_paper.category_urls():
	print(category)
x