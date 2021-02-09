import csv
import matplotlib.pyplot as plt
import os.path

from Ebay.ItemOrganization.eBayQuery import eBayQuery
from Ebay.SiteOperations import printer

from Ebay.ItemOrganization.timer import timer

def make_link(listing_type, search_str):
	"""
	Returns a starting link for a search query.

	>>> make_link("Auction", "Jimi Hendrix Poster")
	'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Jimi Hendrix Poster&LH_Sold=1&LH_Complete=1&rt=nc&LH_Auction=1&_ipg=200'
	>>> make_link("Buy It Now", "Cream Disraeli Gears")
	'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Cream Disraeli Gears&LH_Sold=1&LH_Complete=1&rt=nc&LH_BIN=1&_ipg=200'
	"""
	assert listing_type in ["All Listings", "Auction", "Buy It Now"], "not a valid listing type. Must be one of 'All Listings', 'Auction', or 'Buy It Now'"

	link = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + search_str + "&LH_Sold=1&LH_Complete=1"

	if listing_type == "All Listings":
		pass
	elif listing_type == "Auction":
		link += "&rt=nc&LH_Auction=1"
	elif listing_type == "Buy It Now":
		link += "&rt=nc&LH_BIN=1"

	return link + "&_ipg=200"

def make_csv_name(name, sale_type):
	return r".." + "\\CSV_Collection\\" + name.replace(" ", "_") + f"_{sale_type}.csv"

def make_png_name(name):
	return r"..\ImageDisplay\PNG" + "\\" + name.replace(" ", "_") + "_combo.png"

class queryList:
	"""
	Represents all of the eBay queries we are keeping track of.
	"""
	exportDirectory = r"..\\ItemOrganization\\queryListExport.csv"

	def __init__(self, json):
		self.query_collection = list(queryList.split(json))		

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

	def scrape(self):
		for groupA, groupB, groupC in self.query_collection:
			csv_file = make_csv_name(groupC)

			if os.path.isfile(csv_file):
				collection = ProductCollection.import_data(csv_file)
			else:
				with open(csv_file, "w") as file:
					pass

				collection = ProductCollection(groupA, groupB, groupC)

			for sale_type in ["BIN", "Auction"]:
				fast_download(collection, sale_type, make_link(sale_type, groupC), *cmdline_args) #fast_download takes care of date_stored

			collection.export_data(csv_file)

	def visualize(self):
		for _, __, groupC in self.query_collection:
			csv_file = make_csv_file(groupC)
			png_file = make_png_file(groupC)
			assert os.path.isfile(csv_file)

			collection = ProductCollection.import_data(csv_file)
			collection.graph(png_file, *args, **kwargs)

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

	def set_queries(self, json):
		"""Initializes self.query_collection

		:param json: 
		:rtype: None
		"""

		"""
		for groups in queryList.split(json):
			self.query_collection.append( eBayQuery(*groups) )
		"""
		pass

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


def transfer_csv(q_list):
	import pandas as pd

	for groupA, groupB, groupC in q_list.query_collection:
		#print(groupA, groupB, groupC)
		csv_file = make_csv_name(groupC, "Auction")

		df_a = pd.read_csv(csv_file)
		df_a['date'] = df_a['date'].astype('datetime64[ns]')
		#print(df.dtypes)

		df_a["sale_condition"] = "Auction"
		df_a["groupA"] = groupA
		df_a["groupB"] = groupB
		df_a["groupC"] = groupC

		csv_file = make_csv_name(groupC, "BIN")

		df_b = pd.read_csv(csv_file)
		df_b['date'] = df_b['date'].astype('datetime64[ns]')

		df_b["sale_condition"] = "BIN"
		df_b["groupA"] = groupA
		df_b["groupB"] = groupB
		df_b["groupC"] = groupC

		df_a = df_a[['sale_condition', 'groupA', 'groupB', 'groupC', 'title', 'price', 'date']]
		df_b = df_b[['sale_condition', 'groupA', 'groupB', 'groupC', 'title', 'price', 'date']]

		frames = [df_a, df_b]

		df = pd.concat(frames)
		#print(df)
		#print(df.dtypes)

		csv_final = r".." + "\\CSV_Collection\\" + groupC.replace(" ", "_") + f".csv"
		print(csv_final)

		df.to_csv(csv_final, index = False)


from Ebay.Drivers.json_queries import d
transfer_csv(queryList(d))