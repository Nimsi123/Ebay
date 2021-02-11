import sys

from Ebay.ItemOrganization.queryList import queryList
from Ebay.ItemOrganization.Client import Client
from json_queries import d

def get_kwargs(user_args):
	"""
	:param user_args: The list of user-typed command-line arguments.
	:type user_args: list
	:returns: A dictionary with key:value pairs for kw arguments to driver functions.
	:rtype: dict
	"""
	
	cmd_vals = {
		("print_stats", "-p"): False,
		("deep_scrape", "-d"): False,
		("single_oper", "-s"): False,
		("synchronous_scrape", "-synchr"): False,
	}
	possible_args = [key[1] for key in cmd_vals.keys()]

	not_cmd = [cmd for cmd in user_args if cmd not in possible_args]
	assert not_cmd == [], "Invalid argument: " + str(not_cmd) + ". Choose from: " + str(possible_args)
	
	for kwarg, cmd in cmd_vals:
		if cmd in user_args:
			cmd_vals[(kwarg, cmd)] = True

	kwargs = dict([(kwarg, val) for (kwarg, _), val in cmd_vals.items()])

	return kwargs

if 1:
	Client.reset_csv()
	totalQueries = queryList(d)
	#totalQueries.set_queries(d)
	#totalQueries.data_collection(Client, single_oper = True, deep_scrape = False)
	totalQueries.scrape(Client, single_oper = True, deep_scrape = True)

if __name__ == "__main__" and 0:

	Client.reset_csv()

	kwargs = get_kwargs(sys.argv[1:])

	totalQueries = queryList(d)
	#totalQueries.set_queries(d)
	totalQueries.data_collection(Client, start_index = 145, **kwargs)
	totalQueries.data_visualization(kwargs["single_oper"])