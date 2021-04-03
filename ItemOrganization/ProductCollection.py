import pandas as pd 
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)

class ProductCollection:
	"""Represents a collection of product data scraped from eBayScraper.com.
	Implemented with the pandas module.
	"""

	def __init__(self, csv_file, *groups):
		"""Returns a ProductCollection if the csv_file has a valid length, else if groups are passed to the constructor.
		Otherwise, returns None.

		:param csv_file: The (potential) csv_file to import item data from
		:type csv_file: str
		:param groups: The classification for a specific item.
		:type groups: list of str"""

		df = None
		if os.path.isfile(csv_file):
			df = pd.read_csv(csv_file)

		if df is not None and len(df.index) != 0:
			df['date'] = df['date'].astype('datetime64[ns]')
			self.df = df
			self.groups = [df.loc[0, group] for group in ["groupA", "groupB", "groupC"]]
		else:
			if len(groups) == 0:
				# cannot make a valid ProductCollection
				return

			self.df = pd.DataFrame(columns = ["sale_condition", "groupA", "groupB", "groupC", "title", "price", "date"])
			self.groups = list(groups)


		self.row_count = len(self.df.index)
		self.count_added = 0

	def _valid_item_data(title, price, date, sale_type):
		return type(title) == str and type(price) != str and type(date) != str and type(sale_type) == str

	def _organize_row(self, title, price, date, sale_type):
		"""Returns the proper format for a single row in the pandas DataFrame."""
		return [sale_type] + self.groups + [title, price, date]

	def add_item(self, title, price, date, sale_type):
		"""Adds an item to the collection."""
		assert ProductCollection._valid_item_data(title, price, date, sale_type)

		self.df.loc[self.row_count] = self._organize_row(title, price, date, sale_type)
		self.row_count += 1
		self.count_added += 1

	def get_recent_date(self, sale_type):
		"""Returns the most recent date stored in based on the sale_type. 

		:param sale_type: either 'BIN' or 'Auction'
		:type sale_type: str
		:rtype: pandas.Timestamp or None if there are no items stored
		"""
		assert sale_type in ["BIN", "Auction"]
		if not self.has_valid_length():
			return None

		trimmed_series = self.df[self.df["sale_condition"] == sale_type]["date"].sort_values(ascending = False, ignore_index = True)

		if trimmed_series.empty:
			return None

		return trimmed_series[0]

	def reset_count_added(self):
		"""Resets the counter that tracks the number of items added to storage."""
		self.count_added = 0

	def get_count_added(self):
		"""Returns the number of newly added items."""
		return self.count_added

	def get_row_count(self):
		return self.row_count

	@staticmethod
	def set_axis_details(ax, x_title, y_title, graph_title):

		ax.set(
			xlabel = x_title,
			ylabel = y_title,
			title = graph_title
			)

		formatter = DateFormatter('%m/%d/%y')
		ax.xaxis.set_major_formatter(formatter)
		ax.xaxis.set_tick_params(rotation=30, labelsize=10)

	@staticmethod
	def graph_avg_price(ax, df, sale_condition, dot_color):
		avg_price_df = df[df["sale_condition"] == sale_condition][["date", "price"]].groupby("date").mean().reset_index()
		avg_price_df.plot.scatter("date", "price", c = dot_color, ax = ax, label = sale_condition, rot = 30)

	@staticmethod
	def graph_volume(ax, df, sale_condition, dot_color):
		date_series = df[df["sale_condition"] == sale_condition]["date"]
		volume_df = date_series.value_counts().to_frame().reset_index().rename(columns = {"date": "count", "index": "date"})
		volume_df.plot.scatter("date", "count", c = dot_color, ax = ax, label = sale_condition, rot = 30)

	def scatter(self, png_file):
		"""Creates a scatter plot that overlaps the data from all sale_type(s). Saves the plot to a .png file."""
		if not self.has_valid_length():
			return None

		fig, (avg_price_axes, volume_axes) = plt.subplots(1, 2, figsize=(12,15))

		groupC = self.groups[-1]
		ProductCollection.set_axis_details(avg_price_axes, "date", "average price", groupC)
		ProductCollection.set_axis_details(volume_axes, "date", "volume of sales", groupC)

		auction_details = ("Auction", "lightcoral")
		bin_details = ("BIN", "aquamarine")

		ProductCollection.graph_avg_price(avg_price_axes, self.df, *auction_details)
		ProductCollection.graph_avg_price(avg_price_axes, self.df, *bin_details)
		ProductCollection.graph_volume(volume_axes, self.df, *auction_details)
		ProductCollection.graph_volume(volume_axes, self.df, *bin_details)

		fig.savefig(png_file)
		plt.close()

	def has_valid_length(self):
		return len(self.df.index) != 0

	def export_data(self, csv_file):
		"""Exports data from the underlying data structure to the .csv file. 
		Typically invoked after scraping data.

		:param csv_file: The file to export the data
		:type csv_file: str
		"""
		#remove groupA and groupB from the subset to look at for efficiency?
		#we could even remove groupC, since in these csv file, the group data is all identical!
		#the above assumption might not always be true
		self.df.drop_duplicates(subset = ["sale_condition", "title", "price", "date"]).to_csv(csv_file, index = False)