file = open("urls.txt", "w")
for url in dict['urlList']['results']: 
	file.write(url + "\n") 
file.close()
