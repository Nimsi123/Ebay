import sys
import os
import csv
import matplotlib.pyplot as plt

from Ebay.ItemOrganization.Item import Item
from Ebay.ItemOrganization.Product import ProductList

from Ebay.Site_Operations.ebayFunctions_Grand import getEbayLink


class eBayQuery:
	csvDirectory = r"C:\Users\nimar\AppData\Local\Programs\Python\Python37\Ebay" + "\\"
	pngDirectory = r"C:\Users\nimar\Desktop\ImageDisplay\PNG" + "\\"

	def __init__(self, nombre, enlaceAll = None, enlaceAuction = None, enlaceBIN = None):
		self.name = nombre

		self.csvProductList = eBayQuery.csvDirectory + "CSV_Collection\\" + self.name.replace(" ", "_") + ".csv"
		self.csvProductListAuction = eBayQuery.csvDirectory + "CSV_Collection\\" + self.name.replace(" ", "_") + "_Auction" + ".csv"
		self.csvProductListBIN = eBayQuery.csvDirectory + "CSV_Collection\\" + self.name.replace(" ", "_") + "_BIN" + ".csv"

		self.pngAveragePrice = eBayQuery.pngDirectory + self.name.replace(" ", "_") + "_avgPrice.png"
		self.pngVolume = eBayQuery.pngDirectory + self.name.replace(" ", "_") + "_volume.png"
		self.pngCombo = eBayQuery.pngDirectory + self.name.replace(" ", "_") + "_combo.png"
		self.fileCheck()

		#links are either all there, or not at all
		#after passing through the constructor, the links will all be present
		if enlaceAll == None or enlaceAuction == None or enlaceBIN == None:
			self.linkAll = getEbayLink("All Listings", self.name)
			self.linkAuction = getEbayLink("Auction", self.name)
			self.linkBIN = getEbayLink("Buy It Now", self.name)
		else:
			self.linkAll = enlaceAll
			self.linkAuction = enlaceAuction
			self.linkBIN = enlaceBIN

		self.productCollection = ProductList()

	def fileCheck(self):
		for path in [self.csvProductList, self.csvProductListAuction, self.csvProductListBIN, self.pngAveragePrice, self.pngVolume, self.pngCombo]:
			if not os.path.isfile(path):
				with open(path, "w") as file:
					pass

	def graph(self):
		result = self.productCollection.graphData(self.name, self.pngAveragePrice, self.pngVolume)
		#result = self.productCollection.graphDataNumpy(self.name, self.pngAveragePrice, self.pngVolume)

	def graphCombination(self):
		#create the fig
		fig, (avgPriceAx, volumeAx) = plt.subplots(1, 2, figsize=(12,15))

		#introduce Auction data
		self.importProductData(self.csvProductListAuction)
		package = self.productCollection.splitData(self.name)
		if package == False:
			fig.clf()
			plt.close()
			return False
		else:
			(dateList, avgPriceList, volumeList) = package


		ProductList.fillPlot(avgPriceList, avgPriceAx, "days into the past", "average price", self.name, "lightcoral", "firebrick", "Auction")
		ProductList.fillPlot(volumeList, volumeAx, "days into the past", "volume of sales", self.name, "lightcoral", "firebrick")

		#introduct BIN data
		self.productCollection = ProductList()
		self.importProductData(self.csvProductListBIN)
		package = self.productCollection.splitData(self.name)
		if package == False:
			fig.clf()
			plt.close()
			return False
		else:
			(dateList, avgPriceList, volumeList) = package

		ProductList.fillPlot(avgPriceList, avgPriceAx, "days into the past", "average price", self.name, "aquamarine", "teal", "Buy It Now")
		ProductList.fillPlot(volumeList, volumeAx, "days into the past", "volume of sales", self.name, "aquamarine", "teal")

		fig.legend(loc = "upper right")
		#export the fig
		fig.savefig(self.pngCombo)

		fig.clf()
		plt.close()

	def exportProductData(self):
		#calling exportData on the ProductList() object
		self.productCollection.exportData(self.csvProductList)

	def importProductData(self, csvDirectory):
		self.productCollection.importData(csvDirectory)

	def __str__(self):
		message = ""
		message += f"{self.name}\n"
		message += f"{self.csvProductList}\n"
		message += f"{self.pngAveragePrice}\n"
		message += f"{self.pngVolume}\n"
		message += f"{self.linkAll}\n"
		message += f"{self.linkAuction}\n"
		message += f"{self.linkBIN}\n"

		return message


class queryList:
	def __init__(self):
		self.queryCollection = []
		self.exportDirectory = r"..\\queryListExport.csv"

	def addQuery(self, nombre, enlaceAll = None, enlaceAuction = None, enlaceBIN = None):
		self.queryCollection.append( eBayQuery(nombre, enlaceAll, enlaceAuction, enlaceBIN) )

	def exportData(self, append):
		if append == True:
			with open(self.exportDirectory, "a", encoding = "utf-8") as file:
				data = ["name", "queryDataDirectory", "productListDirectory", "AveragePriceDirectory", "VolumeDirectory", "AllListingsLink", "AuctionLink", "BuyItNowLink"]
				csv_writer = csv.DictWriter(file, fieldnames = data)

				for query in self.queryCollection:
					csv_writer.writerow({"name": query.name, "AllListingsLink": query.linkAll, "AuctionLink": query.linkAuction, "BuyItNowLink": query.linkBIN})
		else:
			with open(self.exportDirectory, "w", encoding = "utf-8") as file:
				data = ["name", "queryDataDirectory", "productListDirectory", "AveragePriceDirectory", "VolumeDirectory", "AllListingsLink", "AuctionLink", "BuyItNowLink"]
				csv_writer = csv.DictWriter(file, fieldnames = data)
				csv_writer.writeheader()
				for query in self.queryCollection:
					csv_writer.writerow({"name": query.name, "AllListingsLink": query.linkAll, "AuctionLink": query.linkAuction, "BuyItNowLink": query.linkBIN})

	def importData(self):
		with open(self.exportDirectory, "r", encoding = "utf-8") as file:
			csv_reader = csv.DictReader(file)
			for line in csv_reader:
				self.addQuery(line["name"], line["AllListingsLink"], line["AuctionLink"], line["BuyItNowLink"])

	def __str__(self):
		message = ""
		for query in self.queryCollection:
			message += f"{query}\n"

		return message