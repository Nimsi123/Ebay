import sys, webbrowser, os

from Ebay.ItemOrganization.query_list import query_list
from Ebay.ItemOrganization.Client import Client
from Ebay.data_files.queries import d

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
		("synchronous_scrape", "-synchr"): False,

		("graph", "-g"): False,

		("print_stats", "-p"): False,
		("single_oper", "-so"): False,

		("web", "-web"): False,

		("test", "-t"): False,
		
	}
	possible_args = [key[1] for key in cmd_vals.keys()]

	not_cmd = [cmd for cmd in user_args if cmd not in possible_args]
	assert not_cmd == [], "Invalid argument: " + str(not_cmd) + ". Choose from: " + str(possible_args)
	
	for kwarg, cmd in cmd_vals.keys():
		if cmd in user_args:
			cmd_vals[(kwarg, cmd)] = True

	kwargs = dict([(kwarg, val) for (kwarg, _), val in cmd_vals.items()])

	return kwargs


if __name__ == "__main__":

	kwargs = get_kwargs(sys.argv[1:])
	totalQueries = query_list(d)

	if kwargs["print_stats"]:
		from termcolor import colored
		os.system('color')

	if kwargs["test"]:

		Client.initialize_client()
		totalQueries.scrape(Client, single_oper = True, print_stats = True, deep_scrape = False)
		import sys
		sys.exit()

	if kwargs["scrape"]:
		Client.initialize_client()
		totalQueries.scrape(client, [kwargs[key] for key in ["single_oper", "synchronous_scrape", "print_stats", "deep_scrape"]])
	if kwargs["graph"]:
		totalQueries.visualize(kwargs["single_oper"], kwargs["print_stats"])
	if kwargs["web"]:
		webbrowser.open("file://" + os.path.realpath("web/index.html"))
