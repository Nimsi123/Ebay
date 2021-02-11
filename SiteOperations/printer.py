def new_query(name, count):
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("					New Query 					")
	print("{0:20}: {1}".format("COLLECTING", name))
	print("{0:20}: {1}".format("COUNT INDEX", count))
	print("---------------------------------------------\n")

def start_scrape(name, listing_type):
	print("{0:20}: {1}".format(name, listing_type))

def end_scrape(listing_type, list_len):
	print("Length of " + "{0:20}: {1}".format(listing_type, list_len))

def product_stats(total_listings, max_iteration):
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
	print("					PRODUCT STATS 				")
	print("{0:30}: {1}".format("total_listings", total_listings))
	print("{0:30}: {1}".format("max_iteration", max_iteration))
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")

def page_stats_one(num_item_listings, added, skipped_early, bad, class_code):
	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	print("PAGE STATS")
	
	print("{0:30}: {1}".format("num item listings", num_item_listings))
	print("{0:30}: {1}".format("added", added))
	print("----")
	print("{0:30}: {1}".format("skipped_early", skipped_early))
	print("{0:30}: {1}".format("bad", bad))
	print("{0:30}: {1}".format("class_code", class_code))
	print("----")

def page_stats_two(count, item_list_length, date_appended):
	print("{0:30}: {1}".format("current item_list length", item_list_length))
	print("{0:30}: {1}".format("iter count", count))
	print("{0:30}: {1}".format("EARLIEST DATE", date_appended))

	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")

def overlap(date_appended, date_stored):
	print("-----------------------------------------------")
	print("					Broken the loop		  		  ")
	print("{0:20}: {1}".format("appended", date_appended))
	print("{0:20}: {1}".format("stored", date_stored))
	print("-----------------------------------------------\n")

def error(e):
	print("*********************************************x86")
	print(e)
	print("*********************************************x86")