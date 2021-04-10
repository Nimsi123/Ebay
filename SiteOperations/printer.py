import os
from termcolor import colored

def new_query(name, count):
	opening_lines = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	new_query =     "\t\tNew Query"
	collecting =    "{0:30}: {1}".format("COLLECTING", name)
	count_index =   "{0:30}: {1}".format("COUNT INDEX", count)
	minus_lines = "---------------------------------------------\n"

	print(opening_lines)
	print(colored(new_query, "green"))
	print(colored(collecting, "green"))
	print(colored(count_index, "green"))
	print(minus_lines)

def start_graph(name):
	print("Graphing " + name)

def start_scrape(name, listing_type):
	start_str = "{0:20}: {1}".format(name, listing_type)
	print(colored(start_str, "green"))

def end_scrape(listing_type, total_listings, list_len):
	total_possible = "{0:30}: {1}".format("Total listings", total_listings)
	length_of =      "{0:30}: {1}".format("Length of " + listing_type, list_len)

	color = "green"
	if total_listings == None or list_len < 0.5 * total_listings:
		color = "red"

	print(colored(total_possible, color))
	print(colored(length_of, color))

def product_stats(total_listings, max_iteration):
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
	print("\t\tPRODUCT STATS")
	print("{0:30}: {1}".format("total_listings", total_listings))
	print("{0:30}: {1}".format("max_iteration", max_iteration))
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")

def page_stats_one(num_item_listings, added, skipped_early, bad, class_code):
	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	print("\t\tPAGE STATS")
	
	print("{0:30}: {1}".format("num item listings", num_item_listings))
	print("{0:30}: {1}".format("added", added))
	print("----")
	print("{0:30}: {1}".format("skipped_early", skipped_early))
	bad_str = "{0:30}: {1}".format("bad", bad)
	print(colored(bad_str, "red"))
	print("{0:30}: {1}".format("class_code", class_code))
	print("----")

def page_stats_two(count, item_list_length, date_appended):
	print("{0:30}: {1}".format("current item_list length", item_list_length))
	print("{0:30}: {1}".format("iter count", count))
	print("{0:30}: {1}".format("EARLIEST DATE", date_appended))

	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")

def overlap(date_appended, date_stored):
	minus_lines =     "---------------------------------------------"
	broken_the_loop = "	\tBroken the loop"
	d_appended =      "{0:20}: {1}".format("appended", date_appended)
	d_stored = "{0:20}: {1}".format("stored", date_stored)

	print(minus_lines)
	print(colored(broken_the_loop, "yellow"))
	print(colored(d_appended, "yellow"))
	print(colored(d_stored, "yellow"))
	print(minus_lines + "\n")

def error(e):
	error_bars = "*********************************************"
	print(colored(error_bars, "red"))
	print(e)
	print(colored(error_bars, "red"))