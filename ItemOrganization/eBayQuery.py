import os
import csv

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

from Ebay.ItemOrganization.ProductList import ProductList
from Ebay.Site_Operations.ebayFunctions_Grand import make_eBay_link

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
		self.csv_All = partial + ".csv"
		self.csv_Auction = partial + "_Auction.csv"
		self.csv_BIN = partial + "_BIN.csv"

		partial = eBayQuery.pngDirectory + self.name.replace(" ", "_")
		self.png_avg_price = partial + "_avgPrice.png"
		self.png_volume = partial + "_volume.png"
		self.png_combo = partial + "_combo.png"

		self.file_check()

		#links are either all there, or not at all
		#after passing through the constructor, the links will all be present
		if enlaceAll == None or enlaceAuction == None or enlaceBIN == None:
			self.linkAll = make_eBay_link("All Listings", self.name)
			self.linkAuction = make_eBay_link("Auction", self.name)
			self.linkBIN = make_eBay_link("Buy It Now", self.name)
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

		#for path in [self.csv_All, self.csv_Auction, self.csv_BIN, self.png_avg_price, self.png_volume, self.png_combo]:
		for path in [self.csv_All, self.csv_Auction, self.csv_BIN]:
			if not os.path.isfile(path):
				with open(path, "w") as file:
					pass

	def fill_plot(dates, data, ax, xTitle, yTitle, graphTitle, colScatter, colLine, labeling = None):
		"""
		Helper function to graph_from_csv.
		Given 'data' (list of numbers), fill the axes 'ax.'
		"""

		ax.set(
			xlabel = xTitle,
			ylabel = yTitle,
			title = graphTitle
			)

		#scatter plot
		ax.plot_date(dates, data, c = colScatter, label = labeling)
		formatter = DateFormatter('%m/%d/%y')
		ax.xaxis.set_major_formatter(formatter)
		ax.xaxis.set_tick_params(rotation=30, labelsize=10)

		#linear regression
		X = np.array( list(range(len(dates))) ).reshape(-1, 1)
		Y = np.array( data ).reshape(-1, 1)

		linear_regressor = LinearRegression()  # create object for the class
		linear_regressor.fit(X, Y)  # perform linear regression
		Y_pred = linear_regressor.predict(X)  # make predictions

		ax.plot(dates, Y_pred, color= colLine) #prediction line

	def graph_from_csv(self, csv_file, fig, avg_price_axes, volume_axes, color_one, color_two, listing_type):
		"""
		Given a csv_file to draw item data from, and two axes, 'avg_price_axes' and 'volume_axes,' graphs the data for the csv file to both axes.
		Returns a boolean value, indicating whether a csv_file had any data to plot.
			--> True: plotted some data
			--> False: did not plot data
		"""

		#introduce data
		self.product_collection = ProductList()
		self.product_collection.import_item_data(csv_file)
		package = self.product_collection.split_data()

		if package == False:
			fig.clf()
			plt.close()
			print("nothing for ", self.name)
			return False
		else:
			date_list, avg_price_list, volume_list = package

		#plot data
		eBayQuery.fill_plot(date_list, avg_price_list, avg_price_axes, "date", "average price", self.name, color_one, color_two, listing_type)
		eBayQuery.fill_plot(date_list, volume_list, volume_axes, "date", "volume of sales", self.name, color_one, color_two)

		return True

	def graph_combo(self):
		"""
		Graph the data associated with the eBay query.
		In this method, since we have data across different search queries, like Auctions and BIN, we can overlap graphs from Auction and BIN.
		"""

		fig, (avg_price_axes, volume_axes) = plt.subplots(1, 2, figsize=(12,15))

		graph_collection = (fig, avg_price_axes, volume_axes)
		auction_colors = ("lightcoral", "firebrick")
		bin_colors = ("aquamarine", "teal")

		rv = self.graph_from_csv(self.csv_Auction, *graph_collection, *auction_colors, "Auction")
		if not rv:
			return False

		rv = self.graph_from_csv(self.csv_BIN, *graph_collection, *bin_colors, "Buy It Now")
		if not rv:
			return False

		fig.legend(loc = "upper right")

		fig.savefig(self.png_combo)

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
		message += f"{self.csv_All}\n"
		message += f"{self.png_avg_price}\n"
		message += f"{self.png_volume}\n"
		message += f"{self.linkAll}\n"
		message += f"{self.linkAuction}\n"
		message += f"{self.linkBIN}\n"

		return message