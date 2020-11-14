import os
import csv
import matplotlib.pyplot as plt

from Ebay.ItemOrganization.ProductList import ProductList
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

    def fillPlot(data, ax, xTitle, yTitle, graphTitle, colScatter, colLine, labeling = None):
    	"""
		Helper function to graphCombination.
    	"""

        X = np.array( list(range(len(data))) ).reshape(-1, 1)
        Y = np.array( data ).reshape(-1, 1)

        linear_regressor = LinearRegression()  # create object for the class
        linear_regressor.fit(X, Y)  # perform linear regression
        Y_pred = linear_regressor.predict(X)  # make predictions

        ax.scatter(X, Y, c = colScatter, label = labeling)
        ax.plot(X, Y_pred, color= colLine)
        ax.set_xlabel(xTitle)
        ax.set_ylabel(yTitle)
        ax.set_title(graphTitle)

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