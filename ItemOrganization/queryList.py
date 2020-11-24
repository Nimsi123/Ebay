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
					csv_writer.writerow(self.get_dict_data())
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

	def data_collection(self, client, single_search = False):
	    """
	    Iterate through queries in self.totalQueries. 
	    For every query, scrape data from AUCTION and BUY IT NOW pages, respectively.
	    Export this data to every query's respective csv file.

	    Note:
	        we don't want to be storing all that ProductList() data!
	        tempList will go out of scope and it will be relieved of its memory usage
	    """

	    count = 0
	    
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
	        tempList.new_export(query.csvProductListAuction, ProductList())
	        print("\nlength of AUCTION", len(tempList.itemList))

	        if single_search:
	        	return

	        #data for Buy It Now listings
	        print(f"\n{query.name} BIN")
	        tempList = ProductList()
	        aboutALink(client, query.linkBIN, tempList)
	        tempList.new_export(query.csvProductListBIN, ProductList())
	        print("\nlength of BIN", len(tempList.itemList))



	    print("finished data collection")

	def data_visualization(self):
	    """
		Make a graph for every eBay query.
	    """

	    for query in self.queryCollection:
	        print(query.name)

	        query.graphCombination()

	        #does this line really do anything?
	        del query #don't want to be storing the query in memory

	    print("visualize finished")