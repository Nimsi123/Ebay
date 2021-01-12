from scraper_api import ScraperAPIClient
import pandas as pd
from Ebay.ItemOrganization.timer import timer
"""
city = pd.DataFrame([	['bfb3cb210e50c39d09f82432095a5150', 0], 
						['cbbdd094d7401d8912b09341e37be9b1', 0],
						['c733663048589db82005534b6739c32e', 0],
						['10c2e4d0fef8e45470a5b43b84f15ec0', 0]], columns= ["api_key", "counter"])
city.to_csv('Client.csv')
"""

api_keys = [
	'bfb3cb210e50c39d09f82432095a5150', #nimarahmanian2020@gmail.com
	'cbbdd094d7401d8912b09341e37be9b1', #nimarahmanian8@gmail.com
	'c733663048589db82005534b6739c32e', #nimsi@berkeley.edu
	'10c2e4d0fef8e45470a5b43b84f15ec0', #oxaxe7@gmail.com
]

"""
with open("Client.csv", "w", encoding = "utf-8") as file:
	data = ["api_key", "counter"]
	csv_writer = csv.DictWriter(file, fieldnames = data)
	csv_writer.writeheader()

	for key in api_keys:
		csv_writer.writerow({"api_key": key, })
"""

class Client:

	df = pd.read_csv("Client.csv")

	current_index = 1
	current_client = ScraperAPIClient( api_keys[current_index] )
	counter = df["counter"][current_index]
	counter_limit = 4950

	def next():
		Client.current_index += 1
		if Client.current_index == len(Client.api_keys):
			print("ran out of api requests.")
			import sys
			sys.exit()

		Client.current_client = ScraperAPIClient( Client.api_keys[Client.current_index] )
		Client.counter = 0

	@timer
	def get(url):
		print("{0:30}: {1}\n".format("CLIENT COUNTER", Client.counter))
		if Client.counter > Client.counter_limit:
			Client.next()
		else:
			Client.counter += 1
			Client.df.at[Client.current_index, "counter"] = Client.counter
			Client.df.to_csv("Client.csv")

			return Client.current_client.get(url)

