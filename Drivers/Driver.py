from Ebay.ItemOrganization.queryList import queryList
from Ebay.ItemOrganization.Client import Client
from name_collection import items

client = Client
#print("client counter: ", client.counter)

totalQueries = queryList()

#totalQueries.add_new_queries(items)
#totalQueries.export_query_data()
#totalQueries.remove_old_queries(Cream)

#totalQueries.data_collection(client)
#totalQueries.data_visualization()

#[print(query.name) for query in totalQueries.queryCollection[320:]]
#print(totalQueries.find_count("PlayStation 5"))
#totalQueries.data_collection(client, start_index = 0, single_search = True)
#totalQueries.data_visualization(start_index = 0, single_graph = False)