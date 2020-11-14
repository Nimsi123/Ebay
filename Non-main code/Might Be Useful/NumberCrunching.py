import sys
import datetime

from Ebay.ItemOrganization.Item import *
#Item, ItemList

from Ebay.ItemOrganization.Product import ProductList
from Ebay.GeneralPurpose.MightBeUseful.MonthlyReport import MonthlyReportList

class BuyingOption:
    def __init__(self, purchaseP, perUnitP, percentOfL, quantity):
        #percent of listings available to buy and make that profit
        self.purchasePrice = purchaseP
        self.percentOfListings = percentOfL #what percent of calculators will give me this per unit profit
        self.saleQuantity = int(percentOfL * quantity) #how many could I sell if i buy at this purchase price
        self.perUnitProfit = perUnitP
        self.totalProfit = self.saleQuantity * perUnitP #if I sell the amount of calculators at the perUnitProfit, what is my totalProfit?

class ListOfBuyingOptions:
    def __init__(self, averageSaleP):
        self.listOfOptions = []
        self.averageSalePrice = averageSaleP

    def addOption(self, option):
        self.listOfOptions.append( option )


items = ProductList()
items.importData("ti-83.csv")
items.finishedCollectingListings()

items.makeMonthlyCollection()


#reportList = MonthlyReportList()

#items.makeMonthlyCollection(reportList)

#reportList.plotReportList()