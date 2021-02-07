import pandas as pd 

class ProductCollection:
	"""Represents a collection of product data scraped from eBay.com.
	Implemented with the pandas module."""

	def __init__(self, *groups):

		#should know where to write the scraped data
		#should know where to save the charts
		self.df = pd.DataFrame(columns = ["sale_condition", "groupA", "groupB", "groupC", "title", "price", "date"])
		self.row_count = 0
		self.groups = list(groups)

	def add_item(self, title, price, date, sale_type):
		"""Adds an item to the collection."""
		self.df.loc[self.row_count] = [sale_type] + self.groups + [title, price, date]
		self.row_count += 1

	def get_recent_date(self, sale_type):
		"""Gets the most recent date stored for either 'BIN' or 'Auction'. 
		(Pandas - implemented with the 'group by' idea.)"""
		if self.df.empty:
			return None

		return self.df[self.df["sale_condition"] == sale_type].head(1)["date"]

	@staticmethod
	def read_csv(csv_file):
		"""Loads data from .csv file to the underlying data structure. Returns a new ProductCollection object.
		Design question. Is this the only site of constructing a ProductCollection object?
		~Table().read_table(csv_file)"""
		new = ProductCollection()
		new.df = pd.read_csv(csv_file)

		return new

	def export_data(self, csv_file):
		"""Exports data from the underlying data structure to the .csv file. 
		Typically invoked after scraping data."""
		self.df.to_csv(csv_file, index = False)

	def count_added(sale_type):
		"""Returns the number of newly added items."""
		pass

	def scatter(self, png_file, *args, **kwargs):
		"""Creates a scatter plot that overlaps the data from all sale_type(s). Saves the plot to a .png file."""
		pass


collection = ProductCollection("Phones", "iPhone", "iPhone XS")
for i in range(10):
	collection.add_item("sample title", i + 3, "sample date" + str(i + 3), "Auction")
	collection.add_item("sample title", i, "sample date", "BIN")

#print(collection.df)
#print(collection.get_recent_date("Auction"))
collection.export_data("tester.csv")

new = ProductCollection.read_csv("tester.csv")
print(new.df)

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