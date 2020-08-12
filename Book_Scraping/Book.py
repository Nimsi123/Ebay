import csv

from Ebay.ItemOrganization.Item import *
#Item, ItemList

class Book:
	def __init__(self, titulo, autor):
		self.title = titulo
		self.author = autor

	def getTitle(self):
		return self.title

	def getAuthor(self):
		return self.author

class BookList:
	def __init__(self):
		self.bookList = []

	def addBook(self, titulo, autor):
		self.bookList.append( Book(titulo, autor) )

	def exportData(self, exportFile):
		with open(exportFile, "w", encoding = "utf-8") as file:
			data = ["title", "author"]
			csv_writer = csv.DictWriter(file, fieldnames = data)
			print("writing header")
			csv_writer.writeheader()
			for book in self.bookList:
				csv_writer.writerow({"title": book.getTitle(), "author": book.getAuthor()})

	def importData(self, dataFile):

		with open(dataFile, "r", encoding = "utf-8") as csv_file:
			csv_reader = csv.DictReader(csv_file)
			for line in csv_reader:
				self.addBook(line["title"], line["author"])