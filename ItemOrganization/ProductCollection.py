import pandas as pd 
import numpy as np

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
		self.df.loc[self.row_count] = [sale_type] + self.groups + [title, price, date]
		self.row_count += 1
		self.count_added += 1

	def get_recent_date(self, sale_type):
		"""Gets the most recent date stored for either 'BIN' or 'Auction'. 
		(Pandas - implemented with the 'group by' idea.)"""
		assert sale_type in ["BIN", "Auction"]
		if self.df.empty:
			return None

		trimmed_series = self.df[self.df["sale_condition"] == sale_type]["date"].sort_values(ascending = False, ignore_index = True)
		return trimmed_series[0]

	def reset_count_added(self):
		self.count_added = 0

	def get_count_added(self):
		"""Returns the number of newly added items."""
		return self.count_added

	def get_row_count(self):
		return self.row_count

	def scatter(self, png_file, *args, **kwargs):
		"""Creates a scatter plot that overlaps the data from all sale_type(s). Saves the plot to a .png file."""
		pass

	@staticmethod
	def import_data(csv_file):
		"""Loads data from .csv file to the underlying data structure. Returns a new ProductCollection object.
		Design question. Is this the only site of constructing a ProductCollection object?
		~Table().read_table(csv_file)"""
		new = ProductCollection()
		new.df = pd.read_csv(csv_file)
		new.df['date'] = new.df['date'].astype('datetime64[ns]')

		new.row_count = len(new.df.index)
		new.groups = [new.df.loc[0, group] for group in ["groupA", "groupB", "groupC"]]
		new.count_added = 0

		return new

	def export_data(self, csv_file):
		"""Exports data from the underlying data structure to the .csv file. 
		Typically invoked after scraping data."""
		self.df.to_csv(csv_file, index = False)

def test_code():
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

test_code()

"""Driver code for scraping and graphing.

#initializing csv_file
for groupA, groupB, groupC in self.query_names:
	csv_file = make_csv_file(groupC)
	collection = ProductCollection().read_csv(csv_file)
	collection.set_groups(groupA, groupB, groupC) #temporary method
	collection.export_data()

#scraping
for query_name in self.query_names:
	csv_file = make_csv_file(query_name)
	collection = ProductCollection().read_csv(csv_file)

	for sale_type in [...]:
		fast_download(collection, make_link(query_name, sale_type), *cmdline_args) #fast_download takes care of date_stored

	collection.export_data(csv_file)

#graphing
for query_name in self.query_names:
	csv_file = make_csv_file(query_name)
	png_file = make_png_file(query_name)
	collection = ProductCollection().read_csv(csv_file)
	collection.graph(png_file, *args, **kwargs)
"""