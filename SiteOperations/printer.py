def product_stats(total_listings, max_iteration):
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
	print("PRODUCT STATS")
	print("{0:30}: {1}".format("total_listings", total_listings))
	print("{0:30}: {1}".format("max_iteration", max_iteration))
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")

def page_stats_one(num_item_listings, count_added, count_skipped_early, count_skipped_bad, count_skipped_class_code):
	print("PAGE STATS")
	print("{0:30}: {1}".format("num item listings", num_item_listings))
	print("{0:30}: {1}".format("count added", count_added))
	print("----")
	print("{0:30}: {1}".format("count_skipped_early", count_skipped_early))
	print("{0:30}: {1}".format("count_skipped_bad", count_skipped_bad))
	print("{0:30}: {1}".format("count_skipped_class_code", count_skipped_class_code))
	print("----")

def page_stats_two(count, item_list_length, link, date_appended):
	print("{0:30}: {1}".format("current item_list length", item_list_length))
	print("{0:30}: {1}".format("iter count", count))
	print("{0:30}: {1}".format("link", link))
	print("{0:30}: {1}".format("EARLIEST DATE", date_appended))
	print("--------\n")

def overlap(date_appended, date_stored):
	print("**********************Broken the loop*************************")
	print("appended: ", date_appended)
	print("stored: ", date_stored)
	print("**************************************************************\n")

def new_query(name, count):
	print("###############New Query#####################")
	print("{0:20}: {1}".format("COLLECTING", name))
	print("{0:20}: {1}".format("COUNT INDEX", count))
	print("#############################################\n")
