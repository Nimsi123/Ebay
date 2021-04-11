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
		if os.path.isfile(BAD_LISTING_DIR):
			self.df = pd.read_csv(BAD_LISTING_DIR)

		if self.df is None:
			self.df = pd.DataFrame(columns = ["title", "price", "shipping", "date"])

	def add(self, title, price, shipping, date):
		self.df = self.df.append({
			"title": title,
			"price": price,
			"shipping": shipping,
			"date": date
			}, 
			ignore_index=True
		)

	def export(self):
		self.df.drop_duplicates().to_csv(BAD_LISTING_DIR, index = None)