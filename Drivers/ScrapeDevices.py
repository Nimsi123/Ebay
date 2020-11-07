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

#sys.exit()
from scraper_api import ScraperAPIClient
client = ScraperAPIClient('c733663048589db82005534b6739c32e')


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




def data_import_new_books():
    totalQueries = queryList()
    for book in bookCollection.bookList:
        totalQueries.addQuery(book.getTitle())

    totalQueries.exportData(append = True)

def whack_shit():
    """
    Print the total number of collected items. How many items are we tracking for every product? How big is the sample size?
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

def data_import():
    #data import sequence

    #load query data into a queryList
    #holds the directories and ebay links
    totalQueries = queryList()
    totalQueries.importData()

    return totalQueries


def data_collection(client, totalQueries):
    #data collection sequence

    count = 0
    
    for query in totalQueries.queryCollection[:1]:
        print("collecting: ", query.name)
        print("count: ", count)
        count += 1

        #we don't want to be storing all that ProductList() data!
        #tempList will go out of scope and it will be relieved of its memory usage

        #data for All listings
        #tempList = ProductList()
        #aboutALink(query.linkAll, tempList)
        #tempList.exportData(query.csvProductList)

        #data for Auction listings
        print(f"\n{query.name} AUCTION")
        tempList = ProductList()
        aboutALink(client, query.linkAuction, tempList)
        #tempList.exportData(query.csvProductListAuction)
        tempList.new_export(query.csvProductListAuction, ProductList())
        print("length for AUCTION", len(tempList.itemList))

        #data for Buy It Now listings
        print(f"\n{query.name} BIN")
        tempList = ProductList()
        aboutALink(client, query.linkBIN, tempList)
        #tempList.exportData(query.csvProductListBIN)
        tempList.new_export(query.csvProductListBIN, ProductList())
        print("length for BIN", len(tempList.itemList))

    print("finished data collection")


def data_visualization(totalQueries):
    #data visualization
    for query in totalQueries.queryCollection[-9:]:
        print(query.name)
        #query.importProductData()
        query.graphCombination()

        del query #don't want to be storing the query in memory

    print("visualize finished")


#sys.exit()
totalQueries = data_import()

data_collection(client, totalQueries)