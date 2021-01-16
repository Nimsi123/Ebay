from Ebay.ItemOrganization.queryList import queryList
from Ebay.ItemOrganization.Client import Client
from name_collection import items

"""
is the following line ever printed when scraping?
this line indicates that eBay is fucking with us, and that we need to take extra precautions to get information from the page.

*****need to do extra work to get sale date********MANDOLORIAN
"""

client = Client
#print("client counter: ", client.counter)

totalQueries = queryList()
# import sys
# sys.exit()
#totalQueries.add_new_queries(items)
#totalQueries.export_query_data()
#totalQueries.remove_old_queries(Cream)

#totalQueries.data_collection(client)
#totalQueries.data_visualization()

#[print(query.name) for query in totalQueries.queryCollection[320:]]
#print(totalQueries.find_count("PlayStation 5"))
totalQueries.data_collection(client, start_index = 1, single_search = True)
#totalQueries.data_visualization(start_index = 1, single_graph = True)



if __name__ == "__main__":
	#totalQueries.data_collection(client)
	#totalQueries.data_visualization()
	pass