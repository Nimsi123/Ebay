from termcolor import colored
from scraper_api import ScraperAPIClient

from eBayScraper.data_files.api_keys import api_keys
#from eBayScraper.ItemOrganization.timer import timer

class Client:

	def next_client():
		"""Once an api key has run out of free requests, switch to the next available api_key. 
		"""

		while (len(Client.data) >= 1 and Client.over_client_limit()):
			Client.data.pop(0)

			if len(Client.data) == 0:
				print(colored("Ran out of api requests!", "red"))
				import sys
				sys.exit()

			Client.current_client, Client.requests = Client.current_client_and_requests()

	def update_counter():
		"""Increments Client.counter and updates .csv file with new counter values."""
		Client.requests += 1

	def over_client_limit():
		return Client.requests >= Client.requests_limit

	def current_client_and_requests():
		return ScraperAPIClient(Client.data[0][0]), Client.data[0][1]

	#@timer
	def get(url):
		"""Essentially a wrapper function to client.get(url). 
		Attempts to get the next client if we're over the current client limit.

		:param url: Downloads the HTML at the url.
		:type url: str
		:returns: The page's HTML
		:rtype: requests.models.Response
		"""

		#print("{0:30}: {1}\n".format("CLIENT COUNTER", Client.counter))

		if Client.over_client_limit():
			Client.next_client()

		attempts = 0
		while attempts < 3:
			try:
				html = Client.current_client.get(url)
				Client.update_counter()
				return html
			except:
				print("Client failed to retrieve HTML.")
				print("Link: " + url)
				attempts += 1

		print(colored("Could not retrieve HTML from link!", "red"))
		import sys
		sys.exit()

	def initialize_client():
		"""Initializes the Client's data before starting up the scraping.
		"""
		Client.data = [(key, ScraperAPIClient(key).account()["requestCount"]) for key in api_keys]
		Client.current_client, Client.requests = Client.current_client_and_requests()
		Client.requests_limit = 1000

	""" 	Miscellaneous 	"""
	def print_usage():
		"""Prints the usage data for every account associated with an API key."""
		for key in api_keys:
			client = ScraperAPIClient(key)
			print(client.account())