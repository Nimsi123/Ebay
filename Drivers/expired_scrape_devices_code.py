def data_import():
    #data import sequence

    #load query data into a queryList
    #holds the directories and ebay links
    totalQueries = queryList()
    totalQueries.importData()

    return totalQueries

def data_collection(client, totalQueries):
    """
    Iterate through queries in totalQueries. 
    For every query, scrape data from AUCTION and BUY IT NOW pages, respectively.
    Export this data to every query's respective csv file.
    """

    count = 236
    
    for query in totalQueries.queryCollection[count:]:
        print("collecting: ", query.name)
        print("count: ", count)
        count += 1

        #we don't want to be storing all that ProductList() data!
        #tempList will go out of scope and it will be relieved of its memory usage

        #data for All listings
        #tempList = ProductList()
        #aboutALink(query.linkAll, tempList)
        #tempList.exportData(query.csvProductList)

        #data for Auction listings
        print(f"\n{query.name} AUCTION")
        tempList = ProductList()
        aboutALink(client, query.linkAuction, tempList)
        tempList.new_export(query.csvProductListAuction, ProductList())
        print("\nlength of AUCTION", len(tempList.itemList))

        #data for Buy It Now listings
        print(f"\n{query.name} BIN")
        tempList = ProductList()
        aboutALink(client, query.linkBIN, tempList)
        tempList.new_export(query.csvProductListBIN, ProductList())
        print("\nlength of BIN", len(tempList.itemList))

    print("finished data collection")


def data_visualization(totalQueries):
    #data visualization
    for query in totalQueries.queryCollection[-9:]:
        print(query.name)
        #query.importProductData()
        query.graphCombination()

        #does this line really do anything?
        del query #don't want to be storing the query in memory

    print("visualize finished")