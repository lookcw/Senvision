dict = 'whatever the dictionary is in the file of urls'

file = open("urls.txt", "w")
for url in dict['urlList']['results']: 
	file.write(url + "\n") 
file.close()
