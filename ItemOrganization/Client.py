from termcolor import colored
from scraper_api import ScraperAPIClient
import pandas as pd

from Ebay.data_files.api_keys import api_keys
from Ebay.data_files.links import CLIENT_REQUESTS_DIR

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
		"""Once an api key has run out of free requests, switch to the next available api_key. 
		Increments Client.current_index, updates Client.current_client, and initializes Client.counter."""

		Client.current_index += 1
		if Client.current_index == len(api_keys):
			print(colored("ran out of api requests.", "red"))
			import sys
			sys.exit()

		Client.current_client = ScraperAPIClient( api_keys[Client.current_index] )
		Client.counter = Client.df["counter"][Client.current_index]

		if Client.counter >= Client.counter_limit:
			Client.next_client()

	def update_counter():
		"""Increments Client.counter and updates .csv file with new counter values."""
		Client.counter += 1

		Client.df.at[Client.current_index, "counter"] = Client.counter
		Client.df.to_csv(CLIENT_REQUESTS_DIR, index = False)

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
		
		#update CLIENT_REQUESTS_DIR
		data = [(key, ScraperAPIClient(key).account()["requestCount"]) for key in api_keys]
		Client.df = pd.DataFrame(data, columns= ["api_key", "counter"])
		Client.df.to_csv(CLIENT_REQUESTS_DIR)

		Client.counter_limit = 1000
		Client.current_index = -1
		Client.next_client()

	""" 	Miscellaneous 	"""
	def print_usage():
		"""Prints the usage data for every account associated with an API key."""
		for key in api_keys:
			client = ScraperAPIClient(key)
			print(client.account())
