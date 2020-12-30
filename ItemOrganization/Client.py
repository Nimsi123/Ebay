from scraper_api import ScraperAPIClient
import csv

api_keys = [
	'bfb3cb210e50c39d09f82432095a5150', #nimarahmanian2020@gmail.com
	'cbbdd094d7401d8912b09341e37be9b1', #nimarahmanian8@gmail.com
	'c733663048589db82005534b6739c32e', #nimsi@berkeley.edu
	'10c2e4d0fef8e45470a5b43b84f15ec0', #oxaxe7@gmail.com
]

with open("Client.csv", "w", encoding = "utf-8") as file:
	data = ["api_key", "counter"]
	csv_writer = csv.DictWriter(file, fieldnames = data)
	csv_writer.writeheader()


class Client:

	current_index = 3
	current_client = ScraperAPIClient( api_keys[current_index] )
	counter = 0
	counter_limit = 4950

	def next():
		Client.current_index += 1
		if Client.current_index == len(Client.api_keys):
			print("ran out of api requests.")
			import sys
			sys.exit()

		Client.current_client = ScraperAPIClient( Client.api_keys[Client.current_index] )
		Client.counter = 0

	def get(url):
		print("{0:30}: {1}".format("CLIENT COUNTER", Client.counter))
		if Client.counter > Client.counter_limit:
			Client.next()
		else:
			Client.counter += 1
			return Client.current_client.get(url)