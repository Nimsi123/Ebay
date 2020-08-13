import sys
import os
import csv

from Ebay.ItemOrganization.Item import Item
from Ebay.ItemOrganization.Product import ProductList

from Ebay.Site_Operations.ebayFunctions_Grand import getEbayLink


class eBayQuery:
	csvDirectory = r"C:\Users\nimar\AppData\Local\Programs\Python\Python37\Ebay" + "\\"
	pngDirectory = r"C:\Users\nimar\Desktop\ImageDisplay\PNG" + "\\"

	def __init__(self, nombre, enlaceAll = None, enlaceAuction = None, enlaceBIN = None):
		self.name = nombre

		self.csvProductList = eBayQuery.csvDirectory + "CSV_Collection\\" + self.name.replace(" ", "_") + ".csv"
		self.pngAveragePrice = eBayQuery.pngDirectory + self.name.replace(" ", "_") + "_avgPrice.png"
		self.pngVolume = eBayQuery.pngDirectory + self.name.replace(" ", "_") + "_volume.png"
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
		for path in [self.csvProductList, self.pngAveragePrice, self.pngVolume]:
			if not os.path.isfile(path):
				with open(path, "w") as file:
					pass

	def graph(self, pdf = None):
		result = self.productCollection.makeMonthlyCollection(self.name, self.pngAveragePrice, self.pngVolume)

		if result != False and pdf != None:
			pdf.add_page()
			pdf.image(self.pngAveragePrice)
			pdf.add_page()
			pdf.image(self.pngVolume)

	def exportProductData(self):
		#calling exportData on the ProductList() object
		self.productCollection.exportData(self.csvProductList)

	def importProductData(self):
		self.productCollection.importData(self.csvProductList)

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
		self.exportDirectory = r"C:\Users\nimar\AppData\Local\Programs\Python\Python37\Ebay\\queryListExport.csv"

	def addQuery(self, nombre, enlaceAll = None, enlaceAuction = None, enlaceBIN = None):
		self.queryCollection.append( eBayQuery(nombre, enlaceAll, enlaceAuction, enlaceBIN) )

	def exportData(self):
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