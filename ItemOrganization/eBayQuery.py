import os
import csv
import matplotlib.pyplot as plt

from Ebay.ItemOrganization.Product import ProductList
from Ebay.Site_Operations.ebayFunctions_Grand import getEbayLink


class eBayQuery:

	"""
	All of the data associated with a single eBay search query.
	Stores data for file directories, such as csv data storage files and png data visualization files.
	"""

	csvDirectory = r".." + "\\CSV_Collection\\"
	pngDirectory = r"..\ImageDisplay\PNG" + "\\"

	def __init__(self, nombre, enlaceAll = None, enlaceAuction = None, enlaceBIN = None):
		self.name = nombre.replace(" ", "_")

		partial = eBayQuery.csvDirectory + self.name
		self.csvProductList = partial + ".csv"
		self.csvProductListAuction = partial + "_Auction.csv"
		self.csvProductListBIN = partial + "_BIN.csv"

		partial = eBayQuery.pngDirectory + self.name
		self.pngAveragePrice = partial + "_avgPrice.png"
		self.pngVolume = partial + "_volume.png"
		self.pngCombo = partial + "_combo.png"

		self.fileCheck()

		#links are either all there, or not at all
		#after passing through the constructor, the links will all be present
		if enlaceAll == None or enlaceAuction == None or enlaceBIN == None:
			self.linkAll = getEbayLink("All Listings", self.name)
			self.linkAuction = getEbayLink("Auction", self.name)
			self.linkBIN = getEbayLink("Buy It Now", self.name)
		else:
			self.linkAll = enlaceAll
			self.linkAuction = enlaceAuction
			self.linkBIN = enlaceBIN

		self.productCollection = ProductList()

	def fileCheck(self):
		"""
		Ensures that all of the files related to the eBay query are available to be written to.
		New files are opened if none exist.
		"""

		#for path in [self.csvProductList, self.csvProductListAuction, self.csvProductListBIN, self.pngAveragePrice, self.pngVolume, self.pngCombo]:
		for path in [self.csvProductList, self.csvProductListAuction, self.csvProductListBIN]:
			if not os.path.isfile(path):
				with open(path, "w") as file:
					pass

	def graphCombination(self):
		"""
		Graph the data associated with the eBay query.
		In this method, since we have data across different search queries, like Auctions and BIN, we can overlap graphs from Auction and BIN.
		"""

		#create the fig
		fig, (avgPriceAx, volumeAx) = plt.subplots(1, 2, figsize=(12,15))

		#introduce Auction data
		self.importProductData(self.csvProductListAuction)
		package = self.productCollection.splitData(self.name)
		if package == False:
			fig.clf()
			plt.close()
			return False
		else:
			(dateList, avgPriceList, volumeList) = package

		#plot Auction data
		ProductList.fillPlot(avgPriceList, avgPriceAx, "days into the past", "average price", self.name, "lightcoral", "firebrick", "Auction")
		ProductList.fillPlot(volumeList, volumeAx, "days into the past", "volume of sales", self.name, "lightcoral", "firebrick")

		#introduct BIN data
		self.productCollection = ProductList()
		self.importProductData(self.csvProductListBIN)
		package = self.productCollection.splitData(self.name)
		if package == False:
			fig.clf()
			plt.close()
			return False
		else:
			(dateList, avgPriceList, volumeList) = package

		#plot BIN data
		ProductList.fillPlot(avgPriceList, avgPriceAx, "days into the past", "average price", self.name, "aquamarine", "teal", "Buy It Now")
		ProductList.fillPlot(volumeList, volumeAx, "days into the past", "volume of sales", self.name, "aquamarine", "teal")

		fig.legend(loc = "upper right")
		#export the fig
		fig.savefig(self.pngCombo)

		#close out
		fig.clf()
		plt.close()

	def get_dict_data(self):
		"""
		Returns a dictionary representation of self.
		"""

		return {"name": query.name, "AllListingsLink": query.linkAll, "AuctionLink": query.linkAuction, "BuyItNowLink": query.linkBIN}

	def __str__(self):
		"""
		Returns a string representation of self.
		"""

		message = ""
		message += f"{self.name}\n"
		message += f"{self.csvProductList}\n"
		message += f"{self.pngAveragePrice}\n"
		message += f"{self.pngVolume}\n"
		message += f"{self.linkAll}\n"
		message += f"{self.linkAuction}\n"
		message += f"{self.linkBIN}\n"

		return message


class queryList:

	"""
	Represents all of the eBay queries we are keeping track of.
	"""

	def __init__(self):
		self.queryCollection = []
		self.exportDirectory = r"..\\queryListExport.csv"

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

	def data_collection(self, client):
	    """
	    Iterate through queries in self.totalQueries. 
	    For every query, scrape data from AUCTION and BUY IT NOW pages, respectively.
	    Export this data to every query's respective csv file.

	    Note:
	        we don't want to be storing all that ProductList() data!
	        tempList will go out of scope and it will be relieved of its memory usage
	    """

	    count = 236
	    
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