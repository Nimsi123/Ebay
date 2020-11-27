import csv
import matplotlib.pyplot as plt

from Ebay.ItemOrganization.ProductList import ProductList
from Ebay.ItemOrganization.eBayQuery import eBayQuery
from Ebay.Site_Operations.ebayFunctions_Grand import *

class queryList:

	"""
	Represents all of the eBay queries we are keeping track of.
	"""

	def __init__(self):
		self.queryCollection = []
		self.exportDirectory = r"..\\ItemOrganization\\queryListExport.csv"

	def find_count(self, search_name):
		"""
		Returns the index of the query in queryCollection that has the title query_name.
		"""

		for i in range(len(self.queryCollection)):
			if self.queryCollection[i].name == search_name:
				return i

	def addQuery(self, nombre, enlaceAll = None, enlaceAuction = None, enlaceBIN = None):
		"""
		Adds an eBayQuery object to self.queryCollection
		Can be used to add new items to track.
		"""

		self.queryCollection.append( eBayQuery(nombre, enlaceAll, enlaceAuction, enlaceBIN) )

	def add_new_queries(self, list_of_names):
		for name in list_of_names:
			self.addQuery(name)

		self.export_query_data(append = True)

	def export_query_data(self, append):
		"""
		Export the data associated with eBayQuery objects to a csv file.
		"""

		with open(self.exportDirectory, "w", encoding = "utf-8") as file:
			data = ["name", "queryDataDirectory", "productListDirectory", "AveragePriceDirectory", "VolumeDirectory", "AllListingsLink", "AuctionLink", "BuyItNowLink"]
			csv_writer = csv.DictWriter(file, fieldnames = data)

			if not append:
				csv_writer.writeheader()

			for query in self.queryCollection:
				csv_writer.writerow( query.get_dict_data() )

	def import_query_data(self):
		"""
		Imports all of the data to do with individual queries from self.exportDirectory
		Populates self.queryCollection with stored queryData.
		"""

		with open(self.exportDirectory, "r", encoding = "utf-8") as file:
			csv_reader = csv.DictReader(file)
			for line in csv_reader:
				self.addQuery(line["name"], line["AllListingsLink"], line["AuctionLink"], line["BuyItNowLink"])

	def __str__(self):
		"""
		Returns a string represention of self
		"""

		return "\n".join([str(query) for query in self.queryCollection])

	def collection_helper(client, name, link, csv_file, listing_type):
		"""
		Helper function to data_collection.
		Populates a ProductList object with item data scraped from the 'link'. Export the data to 'csv_file.'
		"""

	    print(f"\n{name} {listing_type}")

	    tempList = ProductList()
	    aboutALink(client, link, tempList)
	    tempList.export_item_data(csv_file)

	    print(f"\nlength of {listing_type}", len(tempList.item_list))


	def data_collection(self, client, start_index = 0, single_search = False):
	    """
	    Iterate through queries in self.totalQueries. 
	    For every query, scrape data from AUCTION and BUY IT NOW pages, respectively.
	    Export this data to every query's respective csv file.

	    Note:
	        we don't want to be storing all that ProductList() data!
	        tempList will go out of scope and it will be relieved of its memory usage
	    """

	    count = start_index
	    
	    for query in self.queryCollection[count:]:
	        print("collecting: ", query.name)
	        print("count: ", count)
	        count += 1

	        #data for All listings
	        #queryList.collection_helper(client, query.name, query.linkAll, query.csvProductList, "ALL LISTINGS")

	        #data for Auction listings
	        queryList.collection_helper(client, query.name, query.linkAuction, query.csvProductListAuction, "AUCTION")

	        #data for Buy It Now listings
	        queryList.collection_helper(client, query.name, query.linkBIN, query.csvProductListBIN, "BIN")

	        if single_search:
	        	return

	    print("finished data collection")

	def data_visualization(self, start_index, single_graph = False):
	    """
		Make a graph for every eBay query.
	    """

	    for query in self.queryCollection[start_index:]:
	        print(query.name)

	        query.graph_combo()

	        if single_graph:
	        	return

	    print("visualize finished")