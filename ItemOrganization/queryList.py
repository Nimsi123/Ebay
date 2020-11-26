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

		self.exportData(append = True)

	def exportData(self, append):
		if append == True:
			with open(self.exportDirectory, "a", encoding = "utf-8") as file:
				data = ["name", "queryDataDirectory", "productListDirectory", "AveragePriceDirectory", "VolumeDirectory", "AllListingsLink", "AuctionLink", "BuyItNowLink"]
				csv_writer = csv.DictWriter(file, fieldnames = data)

				for query in self.queryCollection:
					csv_writer.writerow(query.get_dict_data())
		else:
			with open(self.exportDirectory, "w", encoding = "utf-8") as file:
				data = ["name", "queryDataDirectory", "productListDirectory", "AveragePriceDirectory", "VolumeDirectory", "AllListingsLink", "AuctionLink", "BuyItNowLink"]
				csv_writer = csv.DictWriter(file, fieldnames = data)
				csv_writer.writeheader()

				for query in self.queryCollection:
					csv_writer.writerow(query.get_dict_data())

	def importData(self):
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
	        #tempList = ProductList()
	        #aboutALink(query.linkAll, tempList)
	        #tempList.exportData(query.csvProductList)

	        #data for Auction listings
	        print(f"\n{query.name} AUCTION")
	        tempList = ProductList()
	        aboutALink(client, query.linkAuction, tempList)
	        tempList.new_export(query.csvProductListAuction)
	        print("\nlength of AUCTION", len(tempList.item_list))

	        if single_search:
	        	return

	        #data for Buy It Now listings
	        print(f"\n{query.name} BIN")
	        tempList = ProductList()
	        aboutALink(client, query.linkBIN, tempList)
	        tempList.new_export(query.csvProductListBIN)
	        print("\nlength of BIN", len(tempList.item_list))

	    print("finished data collection")

	def data_visualization(self):
	    """
		Make a graph for every eBay query.
	    """

	    for query in self.queryCollection:
	        print(query.name)

	        query.graph_combo()

	    print("visualize finished")