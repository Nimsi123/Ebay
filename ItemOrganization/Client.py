from termcolor import colored
from scraper_api import ScraperAPIClient
import pandas as pd

from Ebay.data_files.api_keys import api_keys

from Ebay.ItemOrganization.timer import timer

"""
SOME STATS
fast_download is hitting roughly 130 api requests every 10 minutes.

Threads | Average API Request time

5  | 2.4
10 | 1.4
15 | 1.1
20 | 1.4

Timing before
?

"""
 
class Client:

	def next_client():
		"""Once an api key has run out of free requests, switch clients. 
		Increments Client.current_index, updates Client.current_client, and initializes Client.counter."""

		Client.current_index += 1
		if Client.current_index == len(Client.api_keys):
			print(colored("ran out of api requests.", "red"))
			import sys
			sys.exit()

		Client.current_client = ScraperAPIClient( Client.api_keys[Client.current_index] )
		Client.counter = Client.df["counter"][Client.current_index]

	def update_counter():
		"""Increments Client.counter and updates .csv file with new counter values."""
		Client.counter += 1
		df = pd.read_csv(Client.csv_file)
		df.at[Client.current_index, "counter"] = Client.counter
		df.to_csv(Client.csv_file, index = False)

	#@timer
	def get(url):
		"""Essentially a wrapper function to client.get(url). If the counter exceedes the counter_limit, use the next available client.

		:param url: Downloads the HTML at the url.
		:type url: str
		:returns: The page's HTML
		:rtype: requests.models.Response
		"""

		#print("{0:30}: {1}\n".format("CLIENT COUNTER", Client.counter))

		if Client.counter >= Client.counter_limit:
			Client.next_client()

		Client.update_counter()
		return Client.current_client.get(url)

	def initialize_client():
		"""Initializes the Client's data before starting up the scraping.
		Updates Client.csv with the requestCount number for each api key. 
		"""
		Client.api_keys = api_keys

		Client.csv_file = "data_files/Client.csv"
		Client.df = pd.read_csv(Client.csv_file)
		
		Client.current_index = 6
		Client.current_client = ScraperAPIClient( Client.api_keys[Client.current_index] )
		Client.counter = Client.df["counter"][Client.current_index]
		Client.counter_limit = 1000

		data = [(key, ScraperAPIClient(key).account()["requestCount"]) for key in Client.api_keys]

		df_api_keys = pd.DataFrame(data, columns= ["api_key", "counter"])
		df_api_keys.to_csv( Client.csv_file )

	""" 	Miscellaneous 	"""
	def print_usage():
		"""Prints the usage data for every account associated with an API key."""
		for key in Client.api_keys:
			client = ScraperAPIClient(key)
			print(client.account())
