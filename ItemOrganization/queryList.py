import csv
import matplotlib.pyplot as plt

from Ebay.ItemOrganization.ProductList import ProductList
from Ebay.ItemOrganization.eBayQuery import eBayQuery
from Ebay.SiteOperations.about_a_link import about_a_link
from Ebay.Drivers.fast_download import fast_download

from Ebay.ItemOrganization.timer import timer
from Ebay.SiteOperations import printer

class queryList:
	"""
	Represents all of the eBay queries we are keeping track of.
	"""
	exportDirectory = r"..\\ItemOrganization\\queryListExport.csv"

	def __init__(self):
		self.query_collection = []			

	def data_collection(self, client, start_index = 0, end_index = 999, single_oper = False, synchronous_scrape = False, print_stats = False, deep_scrape = False):
	    """
	    Iterate through queries in self.totalQueries. 
	    For every query, scrape data from AUCTION and BUY IT NOW pages, respectively.
	    Export this data to every query's respective csv file.
	    """

	    cmdline_args = (synchronous_scrape, print_stats, deep_scrape)

	    count = start_index
	    
	    for query in self.query_collection[count:]:
	        printer.new_query(query.name, count)
	        query.scrape(client, *cmdline_args)

	        count += 1
	        #					exclusive
	        if single_oper or count > end_index:
	        	return

	    print("finished data collection")

	@timer
	def data_visualization(self, start_index = 0, single_oper = False):
	    """Makes a graph for every eBay query.

	    :rtype: None
	    """

	    for query in self.query_collection[start_index:]:
	        print(query.name)
	        query.graph_combo()

	        if single_oper:
	        	return

	    print("visualize finished")

	'''
	def sql_export():
		# Larger example that inserts many records at a time

		c.execute("""CREATE TABLE products (name, type, date, price)""")

		for query in self.query_collection:
			for listing_type in ["Auction", "BIN"]:
			data = [query.name, "Auction"]	
		c.executemany('INSERT INTO stocks VALUES (?,?,?,?)', purchases)
	'''

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
	            yield from queryList.split_helper(value, key)

	def split(json):
		"""
		:param json: a json-like dict that holds query information regarding its category
		:type json: dict
		:yields: A tuple consisting of (groupA, groupB, groupC) -- groups that the query falls into.
		:ytype: tuple
		"""
		yield from queryList.split_helper(json)

	def update_queries(self, json):
		"""Ensures that self is up to date with all of the queries to be tracked
		:param json: 
		:rtype: None
		"""
		for groups in queryList.split(json):
			self.query_collection.append( eBayQuery(*groups) )

	""" 	Miscellaneous 	"""
	def __str__(self):
		"""
		Returns a string represention of self
		"""

		return "\n".join([str(query) for query in self.query_collection])

	def find_count(self, search_name):
		"""
		Returns the index of the query in query_collection that has the title query_name.
		"""

		for i in range(len(self.query_collection)):
			if self.query_collection[i].name == search_name:
				return i

	""" 	Mark for Deletion 	"""
	def import_query_data(self):
		"""
		Imports all of the data to do with individual queries from self.exportDirectory
		Populates self.query_collection with stored queryData.
		"""
		assert len(self.query_collection) == 0, "You should not be importing if len(self.query_collection) is not 0. There is a risk of importing overlaps."

		with open(self.exportDirectory, "r", encoding = "utf-8") as file:
			csv_reader = csv.DictReader(file)
			for line in csv_reader:
				grouping = (line["groupA"], line["groupB"], line["groupC"])
				self.addQuery(*grouping)

	def export_query_data(self):
		"""
		Export the data associated with eBayQuery objects to a csv file.
		"""

		with open(self.exportDirectory, "w", encoding = "utf-8") as file:
			data = ["groupA", "groupB", "groupC"]
			csv_writer = csv.DictWriter(file, fieldnames = data)
			csv_writer.writeheader()

			for query in self.query_collection:
				csv_writer.writerow( query.get_dict_data() )

	def remove_old_queries(self, list_of_names):
		"""
		Removes names from a list of existing search queries from the csv file holding data for tracked items.
		"""

		i = 0
		while i < len(self.query_collection):
			query = self.query_collection[i]
			if query.name in list_of_names:
				del self.query_collection[i]
				continue
			i += 1

		self.query_collection.sort(key = lambda query: query.name)
		self.export_query_data()