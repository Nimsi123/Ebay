from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import webbrowser
import time
import sys
import os

from Ebay.ItemOrganization.Item import Item
#from Item import ItemList
from Ebay.ItemOrganization.Product import ProductList

from Ebay.Site_Operations.traverseHtml import *
#findElement, findAllLetters, findKey, findLink

from Ebay.Site_Operations.ebayFunctions_Grand import *
#aboutALink, getEbayLink, is_good_response, log_error, simple_get

from Ebay.Book_Scraping.Book import BookList

from Ebay.ItemOrganization.Product import ProductList

from Ebay.ItemOrganization.FileManagment import fileCheck

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


csvSub = r"C:\Users\nimar\AppData\Local\Programs\Python\Python37\Ebay\Book_Scraping\CSV_Books"
pngSub = r"C:\Users\nimar\Desktop\ImageDisplay\PNG"

#data import sequence
bookCollection = BookList()
path = os.path.join(csvSub, "books.csv")
bookCollection.importData(path)

#making new files
for book in bookCollection.bookList:
	fileCheck(book.getTitle(), False, csvSub, pngSub)


#dig up the starting links, and call aboutALink
xpath = os.path.join(csvSub, "linkBooks.csv")
with open(xpath, "r", encoding = "utf-8") as file:
	csv_reader = csv.DictReader(file)

	count = 0
	for line in csv_reader:
		if count < 71:
			count += 1
			continue
		print(f"{bookCollection.bookList[count].getTitle()}")
		print("link: ", line["link"])

		path = os.path.join(csvSub, f"{bookCollection.bookList[count].getTitle()}.csv")
		aboutALink(line["link"], path)
		count += 1

print("done importing")

pdf = FPDF()

#data visualization/import sequence
listOfProductData = []
for book in bookCollection.bookList:
	path = os.path.join(csvSub, f"{book.getTitle()}.csv")

	tempProduct = ProductList()
	tempProduct.importData(path)
	listOfProductData.append( tempProduct )


for i in range(len(bookCollection.bookList)):
	item = bookCollection.bookList[i].getTitle().replace(" ", "_")
	avgPricePath = os.path.join(pngSub, f"{item}_avgPrice.png")
	volumePath = os.path.join(pngSub, f"{item}_volume.png")

	result = listOfProductData[i].makeMonthlyCollection( item , avgPricePath, volumePath)

	if result == False:
		continue
	else:
		continue
		pdf.add_page()
		pdf.image(avgPricePath)
		pdf.add_page()
		pdf.image(volumePath)

print("done visualizing")

sys.exit()
print("done")
path = os.path.join(r'C:\Users\nimar\AppData\Local\Programs\Python\Python37\Ebay\Book_Scraping', "visualization.pdf")
pdf.output(path, 'F')
webbrowser.open_new(path)










#data collection sequence (names of the books)
"""
link = "https://www.goodreads.com/list/show/8402.Books_Every_High_School_Student_Should_Read"
raw_html = simple_get(link)
html = BeautifulSoup(raw_html, 'html.parser')
bookCollection = BookList()
searchBooks(html, bookCollection)

bookCollection.exportData("books.csv")

print("done")

sys.exit()
"""

"""
#collecting the links
chromedriver = "C:\webdrivers\chromedriver"
driver = webdriver.Chrome(chromedriver)

linkList = []
brokenList = []
for book in bookCollection.bookList:
	try:
		linkList.append( getEbayLink("All Listings", f"{book.getTitle()} {book.getAuthor()} book") )
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