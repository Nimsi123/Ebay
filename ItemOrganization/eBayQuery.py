import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from Ebay.ItemOrganization.ProductList import ProductList
from Ebay.Site_Operations.ebayFunctions_Grand import get_eBay_link


class eBayQuery:

	"""
	All of the data associated with a single eBay search query.
	Stores data for file directories, such as csv data storage files and png data visualization files.
	"""

	csvDirectory = r".." + "\\CSV_Collection\\"
	pngDirectory = r"..\ImageDisplay\PNG" + "\\"

	def __init__(self, nombre, enlaceAll = None, enlaceAuction = None, enlaceBIN = None):
		self.name = nombre

		partial = eBayQuery.csvDirectory + self.name.replace(" ", "_")
		self.csvProductList = partial + ".csv"
		self.csvProductListAuction = partial + "_Auction.csv"
		self.csvProductListBIN = partial + "_BIN.csv"

		partial = eBayQuery.pngDirectory + self.name.replace(" ", "_")
		self.pngAveragePrice = partial + "_avgPrice.png"
		self.pngVolume = partial + "_volume.png"
		self.pngCombo = partial + "_combo.png"

		self.file_check()

		#links are either all there, or not at all
		#after passing through the constructor, the links will all be present
		if enlaceAll == None or enlaceAuction == None or enlaceBIN == None:
			self.linkAll = get_eBay_link("All Listings", self.name)
			self.linkAuction = get_eBay_link("Auction", self.name)
			self.linkBIN = get_eBay_link("Buy It Now", self.name)
		else:
			self.linkAll = enlaceAll
			self.linkAuction = enlaceAuction
			self.linkBIN = enlaceBIN

		self.product_collection = ProductList()

	def file_check(self):
		"""
		Ensures that all of the files related to the eBay query are available to be written to.
		New files are opened if none exist.
		"""

		#for path in [self.csvProductList, self.csvProductListAuction, self.csvProductListBIN, self.pngAveragePrice, self.pngVolume, self.pngCombo]:
		for path in [self.csvProductList, self.csvProductListAuction, self.csvProductListBIN]:
			if not os.path.isfile(path):
				with open(path, "w") as file:
					pass

	def fill_plot(data, ax, xTitle, yTitle, graphTitle, colScatter, colLine, labeling = None):
		"""
		Helper function to graph_from_csv.
		Given 'data' (list of numbers), fill the axes 'ax.'
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

	def graph_from_csv(self, csv_file, fig, avgPriceAx, volumeAx, color_one, color_two, listing_type):
		"""
		Given a csv_file to draw item data from, and two axes, 'avgPriceAx' and 'volumeAx,' graphs the data for the csv file to both axes.
		Returns a boolean value, indicating whether a csv_file had any data to plot.
			--> True: plotted some data
			--> False: did not plot data
		"""

		#introduce data
		self.product_collection = ProductList()
		self.product_collection.importData(csv_file)
		package = self.product_collection.splitData()

		if package == False:
			fig.clf()
			plt.close()
			print("nothing for ", self.name)
			return False
		else:
			(dateList, avgPriceList, volumeList) = package

		#plot data
		avgPriceList = list(reversed(avgPriceList))
		volumeList = list(reversed(volumeList))

		eBayQuery.fill_plot(avgPriceList, avgPriceAx, "days into the past", "average price", self.name, color_one, color_two, listing_type)
		eBayQuery.fill_plot(volumeList, volumeAx, "days into the past", "volume of sales", self.name, color_one, color_two)

		return True

	def graph_combo(self):
		"""
		Graph the data associated with the eBay query.
		In this method, since we have data across different search queries, like Auctions and BIN, we can overlap graphs from Auction and BIN.
		"""

		#create the fig
		fig, (avgPriceAx, volumeAx) = plt.subplots(1, 2, figsize=(12,15))

		rv = self.graph_from_csv(self.csvProductListAuction, fig, avgPriceAx, volumeAx, "lightcoral", "firebrick", "Auction")
		if not rv:
			return False
		rv = self.graph_from_csv(self.csvProductListBIN, fig, avgPriceAx, volumeAx, "aquamarine", "teal", "Buy It Now")
		if not rv:
			return False

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

		return {"name": self.name, "AllListingsLink": self.linkAll, "AuctionLink": self.linkAuction, "BuyItNowLink": self.linkBIN}

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