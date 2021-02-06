import pandas as pd 

class ProductCollection:
	"""Represents a collection of product data scraped from eBay.com.
	Implemented with the pandas module."""

	def __init__(self, group_a, group_b, group_c):

		#should know where to write the scraped data
		#should know where to save the charts
		pass

	def add_item(title, price, date, sale_type):
		"""Adds an item to the collection."""
		pass

	def get_recent_date(sale_type):
		"""Gets the most recent date stored for either 'BIN' or 'Auction'. 
		(Pandas - implemented with the 'group by' idea.)"""
		pass

	def __file_check():
		"""Ensures that there are .csv that we can read and write from."""
		pass

	@staticmethod
	def read_csv(csv_file):
		"""Loads data from .csv file to the underlying data structure. Returns a new ProductCollection object.
		Design question. Is this the only site of constructing a ProductCollection object?
		~Table().read_table(csv_file)"""
		pass

	def export_data(csv_file):
		"""Exports data from the underlying data structure to the .csv file. 
		Typically invoked after scraping data."""
		pass

	def count_added(sale_type):
		"""Returns the number of newly added items."""
		pass

	def scatter(png_file, *args, **kwargs):
		"""Creates a scatter plot that overlaps the data from all sale_type(s). Saves the plot to a .png file."""
		pass



"""Driver code for scraping and graphing.

#scraping
for query_name in self.query_names:
	csv_file = make_csv_file(query_name)
	collection = ProductCollection.read_csv(csv_file)

	for sale_type in [...]:
		fast_download(collection, make_link(query_name, sale_type), *cmdline_args) #fast_download takes care of date_stored

	collection.export_data(csv_file)

#graphing
for query_name in self.query_names:
	csv_file = make_csv_file(query_name)
	png_file = make_png_file(query_name)
	collection = ProductCollection.read_csv(csv_file)
	collection.graph(png_file, *args, **kwargs)
"""