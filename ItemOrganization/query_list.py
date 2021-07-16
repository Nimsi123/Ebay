import csv
import matplotlib.pyplot as plt
import os.path
import pandas as pd 

from eBayScraper.ItemOrganization.ProductCollection import ProductCollection
from eBayScraper.ItemOrganization.BadListings import BadListings
from eBayScraper.SiteOperations import printer
from eBayScraper.SiteOperations.fast_download import fast_download

from eBayScraper.data_files.directories import make_eBay_link, csv_dir, png_dir

"""TODO:

i'm getting way to many "bad" listings

problem with scraping and visualizing with brand new products that have never been scraped before.

ebay brought back the extra keys in the sale date. bring back the key code!

"""

class query_list:
	"""
	Represents all of the eBay queries we are keeping track of.
	"""
	SALE_TYPES = ["BIN", "Auction"]

	def __init__(self, json):
		self.query_collection = list(query_list.split(json)) # (groupA, groupB, groupC)

	def index_of(self, query):
		for i in range(len(self.query_collection)):
			q = self.query_collection[i]
			if q[2] == query:
				return i

		return -1

	def scrape(self, client, start_index = 0, end_index = 999, single_oper = False, synchronous_scrape = False, print_stats = False, deep_scrape = False):

		counter = start_index
		bad_listings = BadListings()
		for groupA, groupB, groupC in self.query_collection[start_index:end_index]:
			printer.new_query(groupC, counter)
			csv_file = csv_dir(groupC)

			collection = ProductCollection(csv_file, groupA, groupB, groupC)

			# scrape
			for sale_type in query_list.SALE_TYPES:
				cmdline_args = (print_stats, deep_scrape)

				if print_stats: 
					printer.start_scrape(groupC, sale_type)
				total_listings = fast_download(client, collection, sale_type, make_eBay_link(sale_type, groupC), bad_listings, *cmdline_args)
				if print_stats:
					printer.end_scrape(sale_type, total_listings, collection.get_count_added())

			collection.export_data(csv_file)
			bad_listings.export()
			counter += 1

			if single_oper:
				return

	def visualize(self, start_index = 0, single_oper = False, print_stats = False):
		for _, __, groupC in self.query_collection[start_index:]:
			if print_stats:
				printer.start_graph(groupC)

			csv_file, png_file = csv_dir(groupC), png_dir(groupC)

			collection = ProductCollection(csv_file)

			if collection:
				collection.scatter(png_file)

			if single_oper:
				return

	""" 	JSON -> eBayQuery 	"""
	def split_helper(json, groupA = None):
	    #helper method to split
	    for key, value in json.items():
	        if type(value) == list:
	            if not groupA:
	                groupA = key
	            for sub in value:
	                yield (groupA, key, sub)
	        else:
	            yield from query_list.split_helper(value, groupA)

	def split(json):
		"""
		:param json: a json-like dict that holds query information regarding its category
		:type json: dict
		:yields: A tuple consisting of (groupA, groupB, groupC) -- groups that the query falls into.
		:ytype: tuple
		"""
		yield from query_list.split_helper(json)

	def aggregate_csv(self):
		"""Aggregates data across csv files into a single csv file."""

		frames = []
		for groupA, groupB, groupC in self.query_collection:
			csv_file = csv_dir(groupC)
			collection = ProductCollection(csv_file, groupA, groupB, groupC)
			frames.append(collection.df)

		aggregated_df = pd.concat(frames)
		aggregated_df.to_csv("aggregate.csv", index = False)


	'''
	def sql_export():
		# Larger example that inserts many records at a time

		c.execute("""CREATE TABLE products (name, type, date, price)""")

		for query in self.query_collection:
			for listing_type in ["Auction", "BIN"]:
			data = [query.name, "Auction"]	
		c.executemany('INSERT INTO stocks VALUES (?,?,?,?)', purchases)
	'''