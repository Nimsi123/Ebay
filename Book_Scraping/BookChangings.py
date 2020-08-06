from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import webbrowser
import time
import sys

from Item import Item
#from Item import ItemList
from Product import ProductList

from traverseHtml import findElement
from traverseHtml import findAllLetters
from traverseHtml import findClassName
from traverseHtml import findKey
from traverseHtml import findLink

from Book import BookList

from ebayFunctions_Grand import aboutALink
from ebayFunctions_Grand import is_good_response
from ebayFunctions_Grand import log_error
from ebayFunctions_Grand import simple_get


def extractBook(html, elementType, attributeKey, attributeValue):
    #this function will return algorithm-friendly data that is in the html block

    raw = findElement(html, elementType, attributeKey, attributeValue)
    
    if raw == "nothing found":
        #bad listing
        return False
    elif type(raw) == str:
        #raw is in a usable form as is
        fruit = raw
    else:
        fruit = raw.contents


    try:
        fruit = fruit[1].contents[0]
    except:
        fruit = fruit[0].contents[0]

    #print("fruit: ", fruit)
    #print("fruit: ", fruit[1].contents[0])

    return fruit

def searchBooks(html, bookCollection, elementType = "tr"):
    #find all "elementType" HTML elements

    for listing in html.find_all(elementType):
    	#loop through all <tr> blocks
    	#extract: title, author

    	#extract: title

    	title = extractBook(listing, "a", "class", "bookTitle")

    	author = extractBook(listing, "a", "class", "authorName")

    	#print(f"{title}: {author}")
    	bookCollection.addBook(title, author)


    return bookCollection

link = "https://www.goodreads.com/list/show/8402.Books_Every_High_School_Student_Should_Read"

def getEbayLink(driver, searchString):

	driver.get("https://www.ebay.com")

	inputBox = driver.find_element_by_id("gh-ac")
	inputBox.send_keys(searchString)

	button = driver.find_elements_by_xpath("//input[@type = 'submit' and @class = 'btn btn-prim gh-spr']")[0]
	button.click()

	#button = driver.find_elements_by_xpath("//input[@class='checkbox__control' and @aria-label='Sold Items']")[0]
	#button = driver.find_elements_by_xpath("//input[@aria-label='Sold Items']")[0]
	#button.click()

	#replace above code with:
	link = driver.current_url
	cutStart = link.find("&_trksid=")
	cutEnd = link.find("&_nkw=")
	newLink = link[:cutStart] + link[cutEnd:] + "&rt=nc&LH_Sold=1&LH_Complete=1"

	#print("return value: ", newLink + "&_ipg=200")

	return newLink + "&_ipg=200"




#data collection sequence (names of the books)
"""raw_html = simple_get(link)
html = BeautifulSoup(raw_html, 'html.parser')
bookCollection = BookList()
searchBooks(html, bookCollection)

bookCollection.exportData("books.csv")

print("done")

sys.exit()"""

#data import sequence
bookCollection = BookList()
bookCollection.importData("books.csv")

print("done importing")

"""
#making new files
for book in bookCollection.bookList:
	with open(f"{book.getTitle()}.csv", "w") as file:
	    pass
print("done making files")
"""

"""
#collecting the links
chromedriver = "C:\webdrivers\chromedriver"
driver = webdriver.Chrome(chromedriver)

linkList = []
brokenList = []
for book in bookCollection.bookList:
	try:
		linkList.append( getEbayLink(driver, f"{book.getTitle()} {book.getAuthor()} book") )
	except:
		brokenList.append(f"{book.getTitle()} {book.getAuthor()}")
		break

with open("link.csv", "w", encoding = "utf-8") as file:
	data = ["link"]
	csv_writer = csv.DictWriter(file, fieldnames = data)
	print("writing header")
	csv_writer.writeheader()
	for link in linkList:
		csv_writer.writerow({"link": link})


for item in brokenList:
	print(item)

print("done for good")
"""

#sys.exit()

chromedriver = "C:\webdrivers\chromedriver"
driver = webdriver.Chrome(chromedriver)

#dig up the starting links, and call aboutALink
with open("link.csv", "r", encoding = "utf-8") as file:
	csv_reader = csv.DictReader(file)
	count = 0
	for line in csv_reader:
		print("link: ", line["link"])
		aboutALink(line["link"], f"{bookCollection.bookList[count].getTitle()}.csv", driver)
		print(f"done with {bookCollection.bookList[count].getTitle()}")
		count += 1

#data collection sequence (eBay data)
print("here")
#aboutALink("https://www.ebay.com/sch/i.html?_from=R40&_nkw=ti-83+calculators&_sacat=0&_ipg=200&LH_Sold=1&LH_Complete=1&rt=nc&LH_All=1", "fake.csv")
print("out")

