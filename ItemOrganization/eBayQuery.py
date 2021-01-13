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

from Ebay.ItemOrganization.timer import timer

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
		"""Ensures that all of the files related to the eBay query exist. New files are opened if one does not exist."""

		#for path in [self.csv_All, self.csv_Auction, self.csv_BIN, self.png_avg_price, self.png_volume, self.png_combo]:
		for path in [self.csv_All, self.csv_Auction, self.csv_BIN]:
			if not os.path.isfile(path):
				with open(path, "w") as file:
					pass

	def fill_plot(dates, data, ax, x_title, y_title, graph_title, color_scatter, color_line, labeling = None):
		"""Helper function to graph_from_csv. Given 'data' (list of numbers), fill the axes 'ax.'
		"""

		ax.set(
			xlabel = x_title,
			ylabel = y_title,
			title = graph_title
			)

		#scatter plot
		ax.plot_date(dates, data, c = color_scatter, label = labeling)
		formatter = DateFormatter('%m/%d/%y')
		ax.xaxis.set_major_formatter(formatter)
		ax.xaxis.set_tick_params(rotation=30, labelsize=10)

		#linear regression
		X = np.array( list(range(len(dates))) ).reshape(-1, 1)
		Y = np.array( data ).reshape(-1, 1)

		linear_regressor = LinearRegression()  # create object for the class
		linear_regressor.fit(X, Y)  # perform linear regression
		Y_pred = linear_regressor.predict(X)  # make predictions

		ax.plot(dates, Y_pred, color= color_line) #prediction line

	def graph_from_csv(self, csv_file, fig, avg_price_axes, volume_axes, color_scatter, color_line, listing_type):
		"""Helper method to self.graph_combo.

		:param csv_file: address of a csv file that stores item data.
		:type csv_file: str
		:param fig: ?
		:type fig: ?
		:param avg_price_axes: Axis for average price data
		:type avg_price_axes: ?
		:param volume_axes: Axis for volume of sales data
		:type volume_axes: ?
		:param color_scatter: The color for the scatter points
		:type color_scatter: str
		:param color_line: The color for the regression line
		:type color_line: str
		:param listing_type: The search query type. Either "Auction" or "Buy It Now"
		:type listing_type: str
		:returns: True if there was data to plot and False otherwise
		:rtype: bool
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
		graph_colors = (color_scatter, color_line)

		x_y_data = (date_list, avg_price_list)
		graph_labels = ("date", "average price", self.name)
		eBayQuery.fill_plot(*x_y_data, avg_price_axes, *graph_labels, *graph_colors, listing_type)

		x_y_data = (date_list, volume_list)
		graph_labels = ("date", "volume of sales",self.name)
		eBayQuery.fill_plot(*x_y_data, volume_axes, *graph_labels, *graph_colors)

		return True

	@timer
	def graph_combo(self):
		"""Graphs the data associated with the eBay query. 
		We overlap the graphs of data from different search queries, like Auction and BIN.
		We make two graphs per query: one for average prices, and one for volume of sales.
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
		"""Returns a dictionary representation of self."""

		return {"name": self.name, "AllListingsLink": self.linkAll, "AuctionLink": self.linkAuction, "BuyItNowLink": self.linkBIN}

	def __str__(self):

		message = f"""{self.name}
		{self.csv_All}
		{self.png_avg_price}
		{self.png_volume}
		{self.linkAll}
		{self.linkAuction}
		{self.linkBIN}"""

		return message

	def __eq__(self, other):
		"""Returns whether two eBay query objects are equivalent. 
		Since all attributes other than self.name are in fact derived from self.name, 
		checking for equality is as simple as checking whether two .name attributes are equal."""

		return self.name == other.name