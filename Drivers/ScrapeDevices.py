import sys
from fpdf import FPDF
import webbrowser
from selenium import webdriver
import os
import csv

from Ebay.ItemOrganization.Item import Item
from Ebay.ItemOrganization.Product import ProductList

from Ebay.Device_Scraping.links_csv_txt import deviceNames

from Ebay.Site_Operations.ebayFunctions_Grand import *
#aboutALink, getEbayLink

from Ebay.ItemOrganization.eBayQuery import queryList

#process of downloading html and iterating over pages
#   request the link and download the html
#   scrape data from the html
#   export the data

#process of importing and displaying the data
#   import the data into a series of ProductList() objects
#   per ProductList() object, graph its contents
#   print all the graphs into a single pdf sheet


#load query data into a queryList
#holds the directories and ebay links
totalQueries = queryList()
totalQueries.importData()

print("import one")

#data collection sequence
for query in totalQueries.queryCollection:
    print("collecting: ", query.name)

    #we don't want to be storing all that ProductList() data!
    #tempList will go out of scope and it will be relieved of its memory usage

    #data for All listings
    tempList = ProductList()
    aboutALink(query.linkAll, tempList)
    tempList.exportData(query.csvProductList)

    #data for Auction listings
    tempList = ProductList()
    aboutALink(query.linkAuction, tempList)
    tempList.exportData(query.csvProductListAuction)

    #data for Buy It Now listings
    tempList = ProductList()
    aboutALink(query.linkBIN, tempList)
    tempList.exportData(query.csvProductListBIN)

print("finished data collection")




#import old ProductList data
#data visualization
for query in totalQueries.queryCollection:
    print(query.name)
    query.importProductData()
    query.graph()
    del query

print("visualize finished")
