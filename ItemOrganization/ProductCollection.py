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
	columns = ["sale_condition", "groupA", "groupB", "groupC", "title", "price", "date"]

	def __init__(self, csv_file, *groups):
		"""Returns a ProductCollection if the csv_file has a valid length, else if groups are passed to the constructor.
		Otherwise, returns None.

		:param csv_file: The (potential) csv_file to import item data from
		:type csv_file: str
		:param groups: The classification for a specific item.
		:type groups: list of str"""

		self.df = None
		if os.path.isfile(csv_file) and not os.stat(csv_file).st_size == 0:
			self.df = pd.read_csv(csv_file)

		if self.df is None or len(self.df.index) == 0:
			if len(groups) == 0:
				# cannot make a valid ProductCollection
				return
			self.df = pd.DataFrame(columns = ProductCollection.columns)
			self.groups = list(groups)
		else:
			self.df['date'] = self.df['date'].astype('datetime64[ns]')
			self.groups = [self.df.loc[0, group] for group in ["groupA", "groupB", "groupC"]]

		self.reset_count_added()
		self.reset_new_entries() # a list of new item data

	def _valid_item_data(title, price, date, sale_type):
		return type(title) == str and type(price) != str and type(date) != str and type(sale_type) == str

	def _organize_row(self, title, price, date, sale_type):
		"""Returns the proper format for a single row in the pandas DataFrame."""
		return [sale_type] + self.groups + [title, price, date]

	def add_item(self, title, price, date, sale_type):
		"""Adds an item to the collection.

		Takes non-trivial time with a large DataFrame (~0.01 seconds).
		Improved time to ~ 5 * 10^-6 seconds. Before, we were adding row by row to the df."""
		assert ProductCollection._valid_item_data(title, price, date, sale_type)

		self.new_entries.append(self._organize_row(title, price, date, sale_type))
		self.count_added += 1

	def has_valid_length(self):
		return len(self.df.index) != 0

	def merge_new_with_stored(self):
		if self.new_entries == []:
			return

		df = pd.DataFrame(self.new_entries, columns = ProductCollection.columns)
		self.df = pd.concat([self.df, df])
		self.reset_new_entries()

	def get_recent_date(self, sale_type):
		"""Returns the most recent date stored in based on the sale_type. 

		:param sale_type: either 'BIN' or 'Auction'
		:type sale_type: str
		:rtype: pandas.Timestamp or None if there are no items stored
		"""
		assert sale_type in ["BIN", "Auction"]

		if self.new_entries != []:
			self.merge_new_with_stored()
		
		if not self.has_valid_length():
			return None

		trimmed_series = self.df[self.df["sale_condition"] == sale_type]["date"].sort_values(ascending = False, ignore_index = True)

		if trimmed_series.empty:
			return None

		return trimmed_series[0]

	def reset_new_entries(self):
		self.new_entries = []

	def reset_count_added(self):
		"""Resets the counter that tracks the number of items added to storage."""
		self.count_added = 0

	def get_count_added(self):
		"""Returns the number of newly added items."""
		return self.count_added

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
		self.merge_new_with_stored()
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

	def export_data(self, csv_file):
		"""Exports data from the underlying data structure to the .csv file. 
		Typically invoked after scraping data.

		:param csv_file: The file to export the data
		:type csv_file: str
		"""
		#remove groupA and groupB from the subset to look at for efficiency?
		#we could even remove groupC, since in these csv file, the group data is all identical!
		#the above assumption might not always be true
		self.merge_new_with_stored()
		self.df.drop_duplicates(subset = ["sale_condition", "title", "price", "date"]).to_csv(csv_file, index = False)