from PyDictionary import PyDictionary
import BeautifulSoup
dictionary=PyDictionary()
dict= (dictionary.synonym("Good"))
for x in dict:
	print dict[x]