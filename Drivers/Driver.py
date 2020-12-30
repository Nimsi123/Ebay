#from Ebay.ItemOrganization.ProductList import ProductList
from Ebay.ItemOrganization.queryList import queryList
from Ebay.ItemOrganization.Client import Client
from Ebay.Site_Operations.ebayFunctions_Grand import aboutALink
from name_collection import *

"""
DESCRIPTION OF HIGH LEVEL OPERATIONS

process of downloading html and iterating over pages
   request the link and download the html
   scrape data from the html
   export the data

process of importing and displaying the data
   import the data into a series of ProductList() objects
   per ProductList() object, graph its contents
   print all the graphs into a single pdf sheet
"""
#set up the web request client

from scraper_api import ScraperAPIClient
#client = ScraperAPIClient('c733663048589db82005534b6739c32e') #nimsi@berkeley.edu
#client = ScraperAPIClient('cbbdd094d7401d8912b09341e37be9b1') #nimarahmanian8@gmail.com
#client = ScraperAPIClient('bfb3cb210e50c39d09f82432095a5150') #nimarahmanian2020@gmail.com
client = Client


#totalQueries = data_import()
#data_collection(client, totalQueries)
#test_export_function(client, totalQueries)
#data_visualization(totalQueries)


totalQueries = queryList()

#totalQueries.add_new_queries(The_Beatles)
#totalQueries.add_new_queries(Cream)
#totalQueries.remove_old_queries(Cream)

#[print(query.name) for query in totalQueries.queryCollection[320:]]
#print(totalQueries.find_count("PlayStation 5"))
totalQueries.data_collection(client, start_index = 210, single_search = False)
#totalQueries.data_visualization(start_index = 0, single_graph = True)