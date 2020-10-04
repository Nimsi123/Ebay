import sys
#from fpdf import FPDF
#import webbrowser
#from selenium import webdriver
import os
import csv
import matplotlib.pyplot as plt

from Ebay.ItemOrganization.Item import Item
from Ebay.ItemOrganization.Product import ProductList
from Ebay.Book_Scraping.Book import BookList

from Ebay.Device_Scraping.links_csv_txt import *

from Ebay.Site_Operations.ebayFunctions_Grand import *
#aboutALink, getEbayLink

from Ebay.ItemOrganization.eBayQuery import queryList
print("running")

#not exporting all the data it's collecting
#something wrong with the export data method

#process of downloading html and iterating over pages
#   request the link and download the html
#   scrape data from the html
#   export the data

#process of importing and displaying the data
#   import the data into a series of ProductList() objects
#   per ProductList() object, graph its contents
#   print all the graphs into a single pdf sheet

"""
#data import sequence


totalQueries = queryList()
for book in bookCollection.bookList:
    totalQueries.addQuery(book.getTitle())

totalQueries.exportData(append = True)
sys.exit()
"""



#load query data into a queryList
#holds the directories and ebay links
totalQueries = queryList()
totalQueries.importData()

#print("import one")

#print(totalQueries.queryCollection[-9])

"""
lengthList = []
count = 0
for query in totalQueries.queryCollection:
    length = 0

    query.importProductData(query.csvProductListAuction)
    length += len(query.productCollection.itemList)

    query.importProductData(query.csvProductListBIN)
    length += len(query.productCollection.itemList)
    #lengthList.append(length)

    if length < 500:
        print(f"{query.name:<30}{length}")
        count += 1
"""


#print(totalQueries.queryCollection[183])



count = 0
#data collection sequence
for query in totalQueries.queryCollection[:1]:
    print("collecting: ", query.name)
    print(count)
    count += 1

    #we don't want to be storing all that ProductList() data!
    #tempList will go out of scope and it will be relieved of its memory usage

    #data for All listings
    #tempList = ProductList()
    #aboutALink(query.linkAll, tempList)
    #tempList.exportData(query.csvProductList)

    #data for Auction listings
    tempList = ProductList()
    aboutALink(query.linkAuction, tempList)
    print("length", len(tempList.itemList))
    tempList.exportData(query.csvProductListAuction)

    #data for Buy It Now listings
    tempList = ProductList()
    aboutALink(query.linkBIN, tempList)
    print("length", len(tempList.itemList))
    tempList.exportData(query.csvProductListBIN)

print("finished data collection")


"""
#import old ProductList data
#data visualization
for query in totalQueries.queryCollection[-9:]:
    print(query.name)
    #query.importProductData()
    query.graphCombination()
    del query

print("visualize finished")
"""
