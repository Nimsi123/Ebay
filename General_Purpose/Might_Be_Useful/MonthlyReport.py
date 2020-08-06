from Item import ItemList
import matplotlib.pyplot as plt

class MonthlyReport(ItemList):
    def __init__(self, dat, itemSubset):
        self.itemList = itemSubset
        self.listOfPrices = []
        self.averagePriceSold = 0
        self.percentUnderAverage = 0

        self.date = dat
        self.volume = len(itemSubset)

        self.makeListOfPrices()
        self.statistics()
        self.findAveragePrice()

class MonthlyReportList:
	def __init__(self):
		self.reportList = []

	def addMonthlyReport(self, monthlyReportObj):
		self.reportList.append(monthlyReportObj)

	def plotReportList(self):

		x_axis = []
		y_axis = []
		for report in self.reportList:

			#x_axis.append( MonthlyReportList.dateToNumber(report.date) )
			x_axis.append( report.date )

			y_axis.append( report.averagePriceSold )

		print("x-axis: ", x_axis)
		print("y-axis: ", y_axis)

		plt.plot(x_axis, y_axis)
		plt.title("Phone Price Change")
		plt.xlabel("Time")
		plt.ylabel("Price")
		plt.show()

#print(MonthlyReportList.dateToNumber("07/02/2020"))

"""
class CollectionOfProductData:
	#this class controls a (2-array)
	#every element in the list corresponds to a product -- the element is a list of MonthlyReport objects

	#the instance of this class will refer to a "zoomed-out" image of phones
	#an iPhone is a suitable object because it has multiple products


	def __init__(self):
		self.modelReportList = []


	def addProductReportList(self, modelMonthlyCollection):
		self.modelReportList.append(modelMonthlyCollection)

	def graphSingleReportList(plt, singleReportList):
		pass

	def makeDiagram():



		for modelReport in self.modelReportList:
			#modelReport is a 1d array that holds MonthlyReport objects
			#every element in modelReport corresponds to a specific month
			pass
"""