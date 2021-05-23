import os
import pandas as pd
from eBayScraper.data_files.directories import BAD_LISTING_DIR

class BadListings:
	"""Instead of loading and writing to bad_listings.csv for every call to 
	search_listings, have an object that keeps track of bad listings, and 
	reads and writes from files less frequently.
	"""
	def __init__(self):

		self.df = None
		if os.path.isfile(BAD_LISTING_DIR) and not os.stat(BAD_LISTING_DIR).st_size == 0:
			self.df = pd.read_csv(BAD_LISTING_DIR)

		if self.df is None or len(self.df.index) == 0:
			self.df = pd.DataFrame(columns = ["title", "price", "shipping", "date"])

		self.new_entries = [] # a list of dictionaries

	def add(self, title, price, shipping, date):
		"""
		Improved time from ~2.5 seconds to 1.6 * 10^-6 seconds. 
		Before, I was appending to a MASSIVE DataFrame.
		"""
		self.new_entries.append({
			"title": title,
			"price": price,
			"shipping": shipping,
			"date": date
			})

	def export(self):
		# concatenate old df with new entries
		df_with_new_entries = pd.DataFrame(self.new_entries)
		self.df = pd.concat([self.df, df_with_new_entries]) # by default, stacks rows on top of each other

		self.df.drop_duplicates().to_csv(BAD_LISTING_DIR, index = None)