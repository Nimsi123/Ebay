class eBayQuery:

	def graph(self):

		result = self.productCollection.graphData(self.name, self.pngAveragePrice, self.pngVolume)
		#result = self.productCollection.graphDataNumpy(self.name, self.pngAveragePrice, self.pngVolume)

	def exportProductData(self, csvDirectory):
		#calling exportData on the ProductList() object
		self.productCollection.exportData(csvDirectory)

	def importProductData(self, csvDirectory):
		#All eBay queries have one productList object. We temporarily populate this list with the data associated with a specific 
		#query, such as Auction or BIN, for example.

		self.productCollection.importData(csvDirectory)