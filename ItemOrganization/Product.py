import csv
import statistics
import datetime

import numpy as np
#from sklearn.linear_model import LinearRegression
#import matplotlib.pyplot as plt

from Ebay.ItemOrganization.Item import *
#Item, ItemList

class ProductList(ItemList):
    def __init__(self):
        self.itemList = []
        self.listOfPrices = []
        self.averagePriceSold = 0
        self.percentUnderAverage = 0

    def addItem(self, item):
        self.itemList.append(item)

    def removePriceOutliers(self, topPrice):
        #make all yuge prices equal to -1
        #all price functions should be adjusted so prices of -1 are not included in any calculation

        i = 0
        while i < len(self.itemList):
            if self.itemList[i].getPrice() >= topPrice:
                #delete the item with the outlier price
                del self.itemList[i]
                i -= 1
            i+= 1

    def getStatsData(self):
        string = ""
        string += f"Mean: {self.mean} "
        string += f"Median: {self.median} "
        string += f"Standard Deviation: {self.stdev}"

        return string

    def countDates(self):
        #all we have is april, may, june, and july
        pass

    def finishedCollectingListings(self):
        #print(self)
        #print("printed self")
        self.makeListOfPrices()
        self.statistics()
        #self.plotHistogram()
        self.findAveragePrice()

    def analyzeAveragePrice(self, profit):
        #assume i sell at the averagePriceSold again
        #then i will make a profit
        
        #purchase_price: the price i would have to buy at to make a profit
        purchase_price = round((0.87)*(self.averagePriceSold)-8 -profit, 2)
        
        total = 0
        for price in self.listOfPrices:
            if price <= purchase_price:
                #a calculator at or below the purchase price is available
                #i can buy this calculator and make a profit
                total += 1

        self.percentAvailable = round(total/len(self.listOfPrices), 2)
        #after ebay and shipping fee's, after profit, how much do i buy calculators for
        #print(f"Buy for purchase price of: {purchase_price} and make a perUnitProfit: ${profit}")
        #print(f"Percent under or at purchase price to buy: {self.percentAvailable}")

        return self.percentAvailable, purchase_price

    def calculateTotalProfit(self, bottom_price):
        #if you buy at the bottom price, you make 0 profit (bottom_price - price)
        #if there is any difference in bottom_price and price, you make a profit
        #the lowest you can buy is (0.87)*(self.averagePriceSold)-8
        #   because of ebay fees and shipping
        
        #bottom_price = round((0.87)*(self.averagePriceSold)-8, 2)

        totalProfit = 0
        for price in self.listOfPrices:
            if price <= bottom_price:
                #a calculator at or below the purchase price is available
                #i can buy this calculator and make a profit
                totalProfit += (bottom_price - price)

        return bottom_price, totalProfit

    def importData(self, dataFile):

        with open(dataFile, "r", encoding = "utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                d = line["date"]
                date = datetime.datetime(int(d[0:4]), int(d[5:7]), int(d[8:10]))
                self.itemList.append( Item(line["title"], float(line["price"]), date ) )

    def date_sort(self):
        self.itemList.sort(key = lambda item: item.date)

    def splitData(self, title):

        #key:value
        #date (mm/dd/yyyy): listOfItems
        reportDictionary = {}

        #put all the sales in a dictionary
        if len(self.itemList) == 0:
            print("nothing for :", title)
            return False

        before_date = self.itemList[0].getDate()
        itemSubset = []
        for item in self.itemList:
            if item.getDate() not in reportDictionary:
                #we have moved onto a new month
                reportDictionary[before_date] = itemSubset
                before_date = item.getDate() #update before_date
                itemSubset = [] #make a new list for the next day

            itemSubset.append(item)
        #for the last entry (it wont enter the last if block)
        reportDictionary[before_date] = itemSubset

        #key:value
        #date: average price sold on this date
        #date: total sales on this date
        reportAverageDictionary = {}
        reportVolumeDictionary = {}

        dateList = []
        avgPriceList = []

        volumeList = []
        for date, itemSubset in reportDictionary.items():
            #store specific values in dictionaries
            avgPrice = statistics.mean([item.getPrice() for item in itemSubset])
            reportAverageDictionary[date] = avgPrice

            reportVolumeDictionary[date] = len(itemSubset)

            #make lists for plotting
            dateList.append(date)
            avgPriceList.append(avgPrice)
            volumeList.append( len(itemSubset) )

        return (dateList, avgPriceList, volumeList)

    def fillPlot(data, ax, xTitle, yTitle, graphTitle, colScatter, colLine, labeling = None):
        X = np.array( list(range(len(data))) ).reshape(-1, 1)
        Y = np.array( data ).reshape(-1, 1)

        linear_regressor = LinearRegression()  # create object for the class
        linear_regressor.fit(X, Y)  # perform linear regression
        Y_pred = linear_regressor.predict(X)  # make predictions

        ax.scatter(X, Y, c = colScatter, label = labeling)
        ax.plot(X, Y_pred, color= colLine)
        ax.set_xlabel(xTitle)
        ax.set_ylabel(yTitle)
        ax.set_title(graphTitle)


    def graphData(self, title, avgPng, volumePng):
        #added histogram

        dateList, avgPriceList, volumeList = self.splitData(title)

        fig = plt.figure(figsize = (5, 4))
        fig = fillPlot(avgPriceList, fig, "days into the past", "average price", title, "red", "red")
        fig.savefig(avgPng)
        #plt.show()
        fig.close()



        fig = plt.figure(figsize = (5, 4))
        fig = fillPlot(volumeList, fig, "days into the past", "volume of sales", title, "red", "red")
        fig.savefig(volumePng)
        #plt.show()
        fig.close()


        """
        plt.figure(figsize = (5, 4))
        plt.hist(avgPriceList)

        plt.xlabel("average price")
        plt.ylabel("number sold")
        plt.title(title)
        plt.show()
        #plt.savefig(avgPng)
        plt.close()
        """