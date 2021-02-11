import pandas as pd 

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)

class ProductCollection:
	"""Represents a collection of product data scraped from eBay.com.
	Implemented with the pandas module."""

	def __init__(self, *groups):

		#should know where to write the scraped data
		#should know where to save the charts
		self.df = pd.DataFrame(columns = ["sale_condition", "groupA", "groupB", "groupC", "title", "price", "date"])
		self.row_count = 0
		self.groups = list(groups)
		self.count_added = 0

	def add_item(self, title, price, date, sale_type):
		"""Adds an item to the collection."""
		assert type(title) == str and type(price) != str and type(date) != str and type(sale_type) == str

		self.df.loc[self.row_count] = [sale_type] + self.groups + [title, price, date]
		self.row_count += 1
		self.count_added += 1

	def get_recent_date(self, sale_type):
		"""Returns the most recent date stored in based on the sale_type. 

		:param sale_type: either 'BIN' or 'Auction'
		:type sale_type: str
		:rtype: pandas.Timestamp or None if there are no items stored
		"""
		assert sale_type in ["BIN", "Auction"]
		if self.df.empty:
			return None

		trimmed_series = self.df[self.df["sale_condition"] == sale_type]["date"].sort_values(ascending = False, ignore_index = True)
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
		avg_price_df.plot.scatter("date", "price", c = dot_color, ax = ax, label = sale_condition)

	@staticmethod
	def graph_volume(ax, df, sale_condition, dot_color):
		volume_df = df[df["sale_condition"] == sale_condition][["date"]]
		volume_df["count"] = 0
		volume_df = volume_df.groupby("date").count().reset_index()
		volume_df.plot.scatter("date", "count", c = dot_color, ax = ax, label = sale_condition)

	def scatter(self, png_file):
		"""Creates a scatter plot that overlaps the data from all sale_type(s). Saves the plot to a .png file."""
		if self.df.empty:
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

	@staticmethod
	def import_data(csv_file):
		"""Loads data from .csv file to the underlying data structure. Returns a new ProductCollection object.
		
		Design question. Is this the only site of constructing a ProductCollection object?
		~Table().read_table(csv_file)

		:param csv_file: The .csv file with the previously scraped data
		:type csv_file: str
		:rtype: ProductCollection
		"""
		new = ProductCollection()
		new.df = pd.read_csv(csv_file)
		new.df['date'] = new.df['date'].astype('datetime64[ns]')

		new.row_count = len(new.df.index)
		new.groups = [new.df.loc[0, group] for group in ["groupA", "groupB", "groupC"]]
		new.count_added = 0

		return new

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

def test_code():
	import numpy as np

	collection = ProductCollection("Phones", "iPhone", "iPhone XS")
	for i in range(0, 10, 2):
		collection.add_item("sample title " + str(i),     i * 2,     np.datetime64("2018-01-1" + str(i)),     "Auction")
		collection.add_item("sample title " + str(i + 1), (i + 1) * 2, np.datetime64("2018-01-1" + str(i + 1)), "BIN")

	assert collection.get_recent_date("Auction") == pd.Timestamp('2018-01-18 00:00:00')
	assert collection.get_recent_date("BIN") == pd.Timestamp('2018-01-19 00:00:00')

	assert collection.get_count_added() == 10
	collection.reset_count_added()
	assert collection.get_count_added() == 0

	for i in range(5):
		collection.add_item("sample title " + str(25 - i),     25 - i,     np.datetime64("2018-01-" + str(25 - i)),     "Auction")

	assert collection.get_count_added() == 5
	assert collection.get_row_count() == 15

	collection.export_data("tester.csv")
	
	collection = ProductCollection.import_data("tester.csv")
	assert collection.get_count_added() == 0
	assert collection.get_row_count() == 15

	assert collection.get_recent_date("Auction") == pd.Timestamp('2018-01-25 00:00:00')
	assert collection.get_recent_date("BIN") == pd.Timestamp('2018-01-19 00:00:00')

#test_code()

def test_display():
	csv_file = r"..\CSV_Collection\ti-83_plus_calculator.csv"
	png_file = r"..\ImageDisplay\PNG\ti-83_plus_calculator.png"

	c = ProductCollection.import_data(csv_file)
	c.scatter(png_file)

test_display()

"""Driver code for scraping and graphing.


#scraping
for groupA, groupB, groupC in self.query_names:
	csv_file = make_csv_file(groupC)

	if (csv_file exists):
		collection = ProductCollection.import_data(csv_file)
	else:
		collection = ProductCollection(groupA, groupB, groupC)

	for sale_type in [...]:
		fast_download(collection, sale_type, make_link(groupC, sale_type), *cmdline_args) #fast_download takes care of date_stored

	collection.export_data(csv_file)

#graphing
for groupA, groupB, groupC in self.query_names:
	csv_file = make_csv_file(groupC)
	png_file = make_png_file(groupC)

	assert (csv_file exists)

	collection = ProductCollection.import_data(csv_file)
	collection.graph(png_file, *args, **kwargs)
"""