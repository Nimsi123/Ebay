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
from Product import ProductList

from cleanEntries import cleanTitle
from cleanEntries import cleanPrice
from cleanEntries import cleanShipping
from cleanEntries import cleanDate
from cleanEntries import stripComma

from traverseHtml import findElement
from traverseHtml import findAllLetters
from traverseHtml import findClassName
from traverseHtml import findKey
from traverseHtml import findLink

from links_csv_txt import linkList
from links_csv_txt import exportFileList
from links_csv_txt import exportHtmlList

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def extract(rawGetFunction, html, elementType, className, cleanFunction):
    #this function will return algorithm-friendly data that is in the html block

    #use the analogy of the coconut
    #html is the entire coconut
    #the coconut fruit can be described with 'elementType' and 'className'
    #rawGetFunction peels away all the extra parts of the coconut and, after some work, we get the fruit
    #cleanFunction will alter the fruit so it is edible


    #html is a subset of the page's entire html we are examining

    #the rawGetFunction zooms in even more on this html and extracts a single HTML element of 'elementType' and 'className'
    #   in the case of finding the sale date, rawGetFunction straight up returns the fruit
    raw = rawGetFunction(html, elementType, className)
    
    if raw == "nothing found":
        #bad listing
        return False
    elif type(raw) == str:
        #raw is in a usable form as is
        fruit = raw
    else:
        fruit = raw.contents

    #nested HTML element?
    try:
        #this means that the item has been sold
        #items that have been sold on ebay have an extra span element NESTED

        fruit = fruit[0].contents[0]
    except:
        #the object is a string, and the element's contents are already accessible
        pass


    #by this point in the code, fruit is the content of the element

    #turn the fruit from ebay into a usable format for my algorithm
    data = cleanFunction(fruit)

    return data

def extractNested(rawGetFunction, html, outerElementType, outerClassName, innerElementType, innerClassName, cleanFunction):
    outerBlock = findElement(html, outerElementType, outerClassName)

    if outerBlock == "nothing found":
        #bad listing
        return False
    else:
        outerBlock = outerBlock.contents

    cleaned_inner = extract(rawGetFunction, outerBlock[0], innerElementType, innerClassName, cleanFunction)

    return cleaned_inner

def searchListings(html, elementType, classCode, itemCollection):
    #find all "elementType" HTML elements
    #extract data to make Item objects
    #search all posted listings and make an ProductList object

    key = findKey(html, elementType)

    for listing in html.find_all(elementType):
        if listing.get("class") == None:
            continue
        else:
            className = (listing.get("class"))[0]

        #the HTML element type is a listing part
        if className == classCode:
            
            #extract the title
            title = extract(findElement, listing, "h3", "s-item__title", cleanTitle)

            #extract the price
            price = extract(findElement, listing, "span", "s-item__price", cleanPrice)

            #extract shipping
            shipping = extract(findElement, listing, "span", "s-item__shipping", cleanShipping)

            #find sale date
            date = extractNested(findAllLetters, listing, "div", "s-item__title--tagblock", "span", key, cleanDate)

            if title == False or price == False or shipping == False or date == False:
                #bad listing
                continue

            #add shipping to price
            itemCollection.addItem( Item(title, round(price+shipping, 2), date) )


def collectLinks(driver, link):

    htmlCodeCollector = []

    count = 0
    #get html and organize it
    raw_html = simple_get(link)
    htmlCodeCollector.append(raw_html)
    count += 1
    print("iter: ", count)

    html = BeautifulSoup(raw_html, 'html.parser')

    total_listings = specialExtractNested(findElement, html, "h1", "srp-controls__count-heading", "span", "BOLD", stripComma)
    max_iteration = int(int(total_listings)/200 +1)

    print("max: ", max_iteration)

    link = 0
    while count < max_iteration:

        #   do work for this page
        #driver.get(link)
        #print("current url: ", driver.current_url)

        #   work for the next page
        link = findLink(html, "a", "pagination__next")

        #get html and organize it
        raw_html = simple_get(link)
        htmlCodeCollector.append(raw_html)
        count += 1
        print("iter: ", count)
        html = BeautifulSoup(raw_html, 'html.parser')

    driver.get(link)
    return htmlCodeCollector

chromedriver = "C:\webdrivers\chromedriver"
#driver = webdriver.Chrome(chromedriver)

#process of downloading html and iterating over pages
#   request the link and download the html
#   while waiting a certain time so num requests per min is low
#       analyze the listings and add onto productCollection
#   when analyzing the page is done
#       if necessary, wait longer before next request
#   make next request, REPEAT





"""
htmlCollection = [] #every element in this list(outer) is a list(inner). the list(inner) has raw_html bytes from all links as elements. the list(outer) represents html data per device
for link in linkList:
    htmlCollection.append( collectLinks(driver, link) )

print("done A")

"""

"""
chromedriver = "C:\webdrivers\chromedriver"

#for i in range(len(exportHtmlList)):
for i in range(2):
    driver = webdriver.Chrome(chromedriver)
    raw_htmlList = collectLinks(driver, linkList[i])
    with open(exportHtmlList[i], "wb") as file:
        for pageHtml in raw_htmlList:
            file.write(pageHtml)

            file.write(b"000000000000000000000000000000000000000000000") #3*15 0's -- termination key for page

        file.write(b"000111000111000111000111000111000111000111000111") #6*8 digits -- termination key for device

print("done B")

"""
for doc in exportHtmlList:
    start = 0
    end = 0
    with open(doc, "rb") as file:
        text = file.read()

        #print(len(text))

        #make the start and end bounds (000111) sequence
        end = text.find(b"000111000111000111000111000111000111000111000111", start)

        termination = text[start:end].find(b"000000000000000000000000000000000000000000000")
        print("termination :", termination)

        count = 0
        while termination != -1:
            count += 1
            termination = text[start:end].find(b"000000000000000000000000000000000000000000000", termination+ len(b"000000000000000000000000000000000000000000000"))
            print("termination :", termination)
            print("count: ", count)
            #input()

        print("done: ", count)

        start = end + len(b"000111000111000111000111000111000111000111000111")

print("done with it all")



"""
with open("delete.txt", "wb") as file:
    for raw_html in raw_html_collection:
        file.write(raw_html)
        file.write(b"000000000000000000000000000000000000000000000") #3*15 0's
print("done")

"""
