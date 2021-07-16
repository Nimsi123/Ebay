import sys, webbrowser, os
from termcolor import colored

from eBayScraper.ItemOrganization.query_list import query_list
from eBayScraper.ItemOrganization.Client import Client
from eBayScraper.data_files.queries import d, to_js_json

def get_kwargs(user_args):
	"""
	:param user_args: The list of user-typed command-line arguments.
	:type user_args: list
	:returns: A dictionary with key:value pairs for kw arguments to driver functions.
	:rtype: dict
	"""
	
	cmd_vals = {
		("scrape", "-s"): False,
		("deep_scrape", "-d"): False,
		("synchronous_scrape", "--synchr"): False,

		("graph", "--graph"): False,

		("print_stats", "--print"): False,
		("single_oper", "-so"): False,

		("web", "--web"): False,

		("test", "--test"): False,
		("setup", "--setup"): False,

		("scrape-test", "--scrape-test"): False,
		
	}
	possible_args = [key[1] for key in cmd_vals.keys()]

	not_cmd = [cmd for cmd in user_args if cmd not in possible_args]
	assert not_cmd == [], "Invalid argument: " + str(not_cmd) + ". Choose from: " + str(possible_args)
	
	for kwarg, cmd in cmd_vals.keys():
		if cmd in user_args:
			cmd_vals[(kwarg, cmd)] = True

	kwargs = dict([(kwarg, val) for (kwarg, _), val in cmd_vals.items()])

	return kwargs

def get_subset(d, keys):
	return {key: d[key] for key in keys}

def check_setup():
	"""Prints to the user if their setup is successful.
	"""
	from eBayScraper.data_files.api_keys import api_keys
	from scraper_api import ScraperAPIClient
	
	all_good = True

	if api_keys == [] or d == {}:
		all_good = False

	#validate api keys
	for key in api_keys:
		try:
			ScraperAPIClient(key).account()
		except:
			all_good = False
			break

	os.system('color')
	if all_good:
		print(colored("Setup is successful!", "green"))
	else:
		print(colored("Make sure the list in data_files/api_keys.py and the dictionary in data_files/queries.py are not empty!", "red"))

def run_test():
	"""Runs a basic test on the scraper, grapher, and web interface.
	"""
	
	os.system('color')
	Client.initialize_client()
	totalQueries = query_list(d)
	totalQueries.scrape(Client, start_index = 0, single_oper = True, print_stats = True, deep_scrape = False)
	totalQueries.visualize(single_oper = True, print_stats = True)
	webbrowser.open("file://" + os.path.realpath("web/index.html"))

totalQueries = query_list(d)
totalQueries.aggregate_csv()

if __name__ == "__main__" and False:

	kwargs = get_kwargs(sys.argv[1:])
	totalQueries = query_list(d)
	to_js_json()

	if kwargs["setup"]:
		check_setup()
		import sys
		sys.exit()

	if kwargs["test"]:
		run_test()
		import sys
		sys.exit()

	if kwargs["scrape-test"]:
		run_scrape_test()
		import sys
		sys.exit()

	if kwargs["print_stats"]:
		os.system('color')

	if kwargs["scrape"]:
		Client.initialize_client()
		totalQueries.scrape(Client, **get_subset(kwargs, ["single_oper", "synchronous_scrape", "print_stats", "deep_scrape"]))
	if kwargs["graph"]:
		totalQueries.visualize(**get_subset(kwargs, ["single_oper", "print_stats"]))
	if kwargs["web"]:
		webbrowser.open("file://" + os.path.realpath("web/index.html"))
