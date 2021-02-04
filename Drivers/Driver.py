import sys

from Ebay.ItemOrganization.queryList import queryList
from Ebay.ItemOrganization.Client import Client
from json_queries import d

"""
is the following line ever printed when scraping?
this line indicates that eBay is fucking with us, and that we need to take extra precautions to get information from the page.

*****need to do extra work to get sale date********MANDOLORIAN
"""

#[print(query.name) for query in totalQueries.queryCollection[320:]]
#print(totalQueries.find_count("PlayStation 5"))
#totalQueries.data_collection(client, start_index = 1, single_search = True)
#totalQueries.data_visualization(start_index = 1, single_graph = True)

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


if __name__ == "__main__" and False:

	kwargs = get_kwargs(sys.argv[1:])

	totalQueries = queryList()
	totalQueries.update_queries(d)
	totalQueries.data_collection(Client, **kwargs)
	totalQueries.data_visualization(kwargs["single_oper"])