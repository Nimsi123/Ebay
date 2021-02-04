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

	def __init__(self):
		self.queryCollection = []
		self.exportDirectory = r"..\\ItemOrganization\\queryListExport.csv"

	def find_count(self, search_name):
		"""
		Returns the index of the query in queryCollection that has the title query_name.
		"""

		for i in range(len(self.queryCollection)):
			if self.queryCollection[i].name == search_name:
				return i

	def addQuery(self, *grouping):
		"""
		Adds an eBayQuery object to self.queryCollection
		Can be used to add new items to track.
		"""
		new_query = eBayQuery(*grouping)
		if new_query not in self.queryCollection:
			self.queryCollection.append( new_query )

	def add_new_queries(self, list_of_names):
		"""
		Adds names from a list of new search queries to track to the csv file holding data for tracked items.
		"""
		existing_query_names = [query.name for query in self.queryCollection]

		for name in list_of_names:
			if name not in existing_query_names:
				self.addQuery(name)

		self.queryCollection.sort(key = lambda query: query.name)
		self.export_query_data()

	#mark for deletion
	def remove_old_queries(self, list_of_names):
		"""
		Removes names from a list of existing search queries from the csv file holding data for tracked items.
		"""

		i = 0
		while i < len(self.queryCollection):
			query = self.queryCollection[i]
			if query.name in list_of_names:
				del self.queryCollection[i]
				continue
			i += 1

		self.queryCollection.sort(key = lambda query: query.name)
		self.export_query_data()

	def export_query_data(self):
		"""
		Export the data associated with eBayQuery objects to a csv file.
		"""

		with open(self.exportDirectory, "w", encoding = "utf-8") as file:
			data = ["groupA", "groupB", "groupC"]
			csv_writer = csv.DictWriter(file, fieldnames = data)
			csv_writer.writeheader()

			for query in self.queryCollection:
				csv_writer.writerow( query.get_dict_data() )

	#mark for deletion
	def import_query_data(self):
		"""
		Imports all of the data to do with individual queries from self.exportDirectory
		Populates self.queryCollection with stored queryData.
		"""
		assert len(self.queryCollection) == 0, "You should not be importing if len(self.queryCollection) is not 0. There is a risk of importing overlaps."

		with open(self.exportDirectory, "r", encoding = "utf-8") as file:
			csv_reader = csv.DictReader(file)
			for line in csv_reader:
				grouping = (line["groupA"], line["groupB"], line["groupC"])
				self.addQuery(*grouping)

	def __str__(self):
		"""
		Returns a string represention of self
		"""

		return "\n".join([str(query) for query in self.queryCollection])

	def collection_helper(client, name, link, csv_file, listing_type, date_stored, synchronous_scrape, print_stats, deep_scrape):
		"""
		Helper function to data_collection.
		Populates a ProductList object with item data scraped from the 'link'. Export the data to 'csv_file.'

	    Note:
	        we don't want to be storing all that ProductList() data!
	        temp_list will go out of scope and it will be relieved of its memory usage
		"""

		print(f"{name} {listing_type}\n")

		temp_list = ProductList()

		try:
			if not synchronous_scrape:
				fast_download(client, temp_list, link, date_stored, print_stats, deep_scrape)
			else:
				about_a_link(client, link, temp_list, date_stored)
		except Exception as e:
			print("********************************************************************x86")
			print(e)
			print("********************************************************************x86")
			queryList.collection_helper(client, name, link, csv_file, listing_type, date_stored)


		temp_list.export_item_data(csv_file)

		print(f"length of {listing_type}", len(temp_list.item_list), "\n")

	def get_date_stored(csv_file):
		temp_list = ProductList()
		temp_list.import_item_data(csv_file)
		if temp_list.item_list:
			return temp_list.item_list[-1].date
		return None


	def data_collection(self, client, start_index = 0, end_index = 999, single_oper = False, synchronous_scrape = False, print_stats = False, deep_scrape = False):
	    """
	    Iterate through queries in self.totalQueries. 
	    For every query, scrape data from AUCTION and BUY IT NOW pages, respectively.
	    Export this data to every query's respective csv file.
	    """

	    cmdline_args = (synchronous_scrape, print_stats, deep_scrape)

	    count = start_index
	    
	    for query in self.queryCollection[count:]:
	        printer.new_query(query.name, count)

	        count += 1

	        #queryList.collection_helper(client, query.name, query.linkAll, query.csv_All, "ALL LISTINGS")
	        
	        date_stored = queryList.get_date_stored(query.csv_Auction)
	        query_data = (query.name, query.linkAuction, query.csv_Auction)
	        queryList.collection_helper(client, *query_data, "AUCTION", date_stored, *cmdline_args)

	        date_stored = queryList.get_date_stored(query.csv_BIN)
	        query_data = (query.name, query.linkBIN, query.csv_BIN)
	        queryList.collection_helper(client, *query_data, "BIN", date_stored, *cmdline_args)

	        #					exclusive
	        if single_oper or count > end_index:
	        	return

	    print("finished data collection")

	@timer
	def data_visualization(self, start_index = 0, single_oper = False):
	    """Makes a graph for every eBay query.

	    :rtype: None
	    """

	    for query in self.queryCollection[start_index:]:
	        print(query.name)

	        query.graph_combo()

	        if single_oper:
	        	return

	    print("visualize finished")

	'''
	def sql_export():
	# Larger example that inserts many records at a time

		c.execute("""CREATE TABLE products (name, type, date, price)""")

		for query in self.queryCollection:
			for listing_type in ["Auction", "BIN"]:
			data = [query.name, "Auction"]	
		c.executemany('INSERT INTO stocks VALUES (?,?,?,?)', purchases)
	'''

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
			self.addQuery(*groups)