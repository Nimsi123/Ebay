from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import webbrowser
import time
import sys
from fpdf import FPDF

import functools

from Ebay.ItemOrganization.Item import Item
from Ebay.ItemOrganization.Product import ProductList

from Ebay.Site_Operations.cleanEntries import *
#cleanTitle, cleanPrice, cleanShipping, cleanDate, stripComma

from Ebay.Site_Operations.traverseHtml import *
#findElement, findAllLetters, findKey, findLink

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

def simple_get(url, testing = False):
	try:
		with closing(get(url, stream=True)) as resp:
			if is_good_response(resp):
				if testing:
					return resp.text
				else:
					return resp.content
			else:
				return None
	except RequestException as e:
		log_error('Error during requests to {0} : {1}'.format(url, str(e)))
		return None

"""def simple_get(driver, url):
	driver.get(url)
	return driver.page_source"""




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


def searchListings(html, elementType, classCode, itemCollection):
	#find all "elementType" HTML elements
	#extract data to make Item objects
	#search all posted listings and make an ProductList object


	#ebay tries to mess with the sale date and my code
	#right before the code starts, I will find the special className that can be used to find the sale date!
	key = findKey(html, elementType, ["S", "o", "l", "d"])
	"""if key == None:
					#print("********************************************************************************")
				else:
					print("////////////////////////////////////////////////////////////////////////////////")
					print("key: ", key)
					print("////////////////////////////////////////////////////////////////////////////////")"""

	for listing in html.find_all(elementType):
		if listing.get("class") == None:
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
				continue

			else:
				#good listing

				#add shipping to price
				totalCost = round(price+shipping, 2)
				#print("add item")
				itemCollection.addItem( Item(title, totalCost, date) )

def getEbayLink(listingType, searchString):

	"""
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
	newLink = link[:cutStart] + link[cutEnd:] + "&rt=nc&LH_Sold=1&LH_Complete=1" + "&_ipg=200"

	#print("return value: ", newLink)

	return newLink
	"""

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

def aboutALink(link, productCollection):

	totalTime = 0

	#get html and organize it
	raw_html = simple_get(link)
	html = BeautifulSoup(raw_html, 'html.parser')

	#driver.get(link)
	#html = BeautifulSoup(driver.page_source, 'html.parser')

	total_listings = int(extract(findElement, html, "h1", "srp-controls__count-heading", stripComma))

	#there is nothing for us here
	#print("total_listings: ", total_listings)

	if total_listings == 0:
		return

	max_iteration = int(total_listings/200 +1)


	count = 0
	while count < max_iteration:

		#get html and organize it
		#print("current link: ", link)

		raw_html = simple_get(link, True)
		html = BeautifulSoup(raw_html, 'html.parser')


		#search the listings for data
		searchListings(html, "li", "s-item", productCollection)
		count += 1

		#get the link for the next page
		#print("link: ", link)
		link = findLink(html, "a", "pagination__next")

		#print("count: ", count)

		#if there is no next link, we have reached the end
		if link == "nothing found":
			break