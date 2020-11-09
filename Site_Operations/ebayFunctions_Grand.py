#from requests import get
#from requests.exceptions import RequestException
#from contextlib import closing
from bs4 import BeautifulSoup
#from selenium import webdriver
#import csv
#import webbrowser
#import time
#import sys
#from fpdf import FPDF
#from time import sleep

#import functools

from Ebay.ItemOrganization.Item import Item
from Ebay.ItemOrganization.Product import ProductList

from Ebay.Site_Operations.cleanEntries import *
#cleanTitle, cleanPrice, cleanShipping, cleanDate, stripComma

from Ebay.Site_Operations.traverseHtml import *
#findElement, findAllLetters, findKey, findLink


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
	#print("data in extract: ", elementType, className)
	raw = rawGetFunction(html, elementType, "class", className)
	
	if raw == "nothing found":
		#bad listing
		#print(elementType, className)
		#print("extract none")
		return None
	elif type(raw) == str:
		#raw is in a usable form as is
		fruit = raw
	else:
		fruit = raw.contents

	#nested HTML element?
	try:
		#this means that the item has been sold
		#items that have been sold on ebay have an extra span element NESTED

		fruit = fruit[0].contents
	except:
		#the object is a string, and the element's contents are already accessible
		pass

	if type(fruit) != str:
		try:
			fruit = fruit[0]
		except:
			print("oops")

	#by this point in the code, fruit is the content of the element

	#turn the fruit from ebay into a usable format for my algorithm
	data = cleanFunction(fruit)

	return data

def extractNested(rawGetFunction, html, outerElementType, outerClassName, innerElementType, innerClassName, cleanFunction):
	outerBlock = findElement(html, outerElementType, "class", outerClassName)

	if outerBlock == "nothing found":
		#bad listing
		return None
	else:
		outerBlock = outerBlock.contents

	cleaned_inner = extract(rawGetFunction, outerBlock[0], innerElementType, innerClassName, cleanFunction)

	return cleaned_inner


def searchListings(html, elementType, classCode, itemCollection, printer_bool_page_stats):
	#find all "elementType" HTML elements
	#extract data to make Item objects
	#search all posted listings and make an ProductList object


	#ebay tries to mess with the sale date and my code
	#right before the code starts, I will find the special className that can be used to find the sale date!
	key = findKey(html, elementType, ["S", "o", "l", "d"])

	count = 0
	count_skipped_early = 0
	count_skipped_bad = 0
	count_skipped_classcode = 0
	for listing in html.find_all(elementType):
		if listing.get("class") == None:
			count_skipped_early += 1
			continue
		else:
			className = (listing.get("class"))[0]

		#the HTML element type is a listing part
		if className == classCode:
			#in this block, we extract data from a single listing
			

			#extract the title
			title = extract(findElement, listing, "h3", "s-item__title", cleanTitle)

			#extract the price
			price = extract(findElement, listing, "span", "s-item__price", cleanPrice)

			#extract shipping
			shipping = extract(findElement, listing, "span", "s-item__shipping", cleanShipping)

			#find sale date
			if key == None:
				date = extract(findElement, listing, "div", "s-item__title--tagblock", cleanDate)
			else:
				date = extractNested(findAllLetters, listing, "div", "s-item__title--tagblock", "span", key, cleanDate)


			if title == None or price == None or shipping == None or date == None:
				#bad listing
				#print(f"title: {title} price: {price} shipping: {shipping} date: {date}")
				#print("bad listing")
				count_skipped_bad += 1
				continue

			else:
				#good listing

				#add shipping to price
				totalCost = round(price+shipping, 2)
				#print("add item")
				count += 1
				itemCollection.addItem( Item(title, totalCost, date) )
		else:
			count_skipped_classcode += 1

	if printer_bool_page_stats:
		print("\n")
		print("PAGE STATS")
		print(f"num item listings: {len(html.find_all(elementType))}")
		print(f"count added: {count}")
		print(f"count_skipped_early: {count_skipped_early} ... count_skipped_bad: {count_skipped_bad} ... count_skipped_classcode: {count_skipped_classcode}")

def getEbayLink(listingType, searchString):

	link = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + searchString + "&LH_Sold=1&LH_Complete=1"

	if listingType == "All Listings":
		pass
	elif listingType == "Auction":
		link += "&rt=nc&LH_Auction=1"
	elif listingType == "Buy It Now":
		link += "&rt=nc&LH_BIN=1"
	else:
		print("bad listingType")

	return link + "&_ipg=200"

def receive_html(client, link):
	"""
	Returns the html from a webpage as a BeautifulSoup object.
	"""

	raw_html = client.get(url = link).text
	html = BeautifulSoup(raw_html, 'html.parser')

	return html


def aboutALink(client, link, productCollection):
	printer_bool_product_stats = True
	printer_bool_page_stats = True

	html = receive_html(client, link)

	print("extract: ", extract(findElement, html, "h1", "srp-controls__count-heading", stripComma))
	total_listings = int(extract(findElement, html, "h1", "srp-controls__count-heading", stripComma))

	if total_listings == 0:
		return

	max_iteration = min(50, int(total_listings/200 +1)) #ebay won't show us more that 10,000 items from their page even though there might be more to look at

	if printer_bool_product_stats:
		print("\nPRODUCT STATS")
		print("total_listings: ", total_listings)
		print("max_iteration", max_iteration)

	for count in range(max_iteration):

		html = receive_html(client, link)
		searchListings(html, "li", "s-item", productCollection, printer_bool_page_stats) #search the listings for data. populate the productCollection list

		if printer_bool_page_stats:
			print(f"iter count: {count} ... current itemList length: {len(productCollection.itemList)}")
			print(f"link: {link}")

		link = findLink_new(link) #get the link for the next page