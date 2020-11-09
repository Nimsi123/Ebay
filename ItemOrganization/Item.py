import matplotlib.pyplot as plt
import statistics
import csv
import datetime
import statistics

class Item:
    def __init__(self, t, p, d):
        self.title = t
        self.price = p
        self.date = d

    def __str__(self):
        return f"{self.getTitle()} {self.getPrice()} {self.getDate()}"

    def getTitle(self):
        return self.title

    def getPrice(self):
        return self.price

    def getDate(self):
        return self.date

    def get_dict_data(self):
        return {"title": self.title, "price": self.price, "date": self.date}

    def __eq__(self, other):
        return self.title == other.title and self.price == other.price and self.date == other.date

class ItemList:
    """
    def __init__(self):
        self.itemList = []
        self.listOfPrices = []
        self.averagePriceSold = 0
        self.percentUnderAverage = 0

    def __init__(self, dat, itemSubset):
        self.itemList = itemSubset
        self.listOfPrices = [item.getPrice() for item in self.itemList]
        self.averagePriceSold = statistics.mean(self.listOfPrices)
        self.percentUnderAverage = 0
        self.date = dat

        self.makeListOfPrices()
        self.statistics()
        self.findAveragePrice()
    """

    def make_stats(self):
        self.mean = round(statistics.mean(self.listOfPrices), 2)
        self.median = round(statistics.median(self.listOfPrices), 2)
        self.stdev = round(statistics.stdev(self.listOfPrices), 2)

    def getStatsData(self):
        string = ""
        string += f"Mean: {self.mean} "
        string += f"Median: {self.median} "
        string += f"Standard Deviation: {self.stdev}"

        return string

    def plotHistogram(self):
        prices = self.getListOfPrices()
        stretch = max(prices) - min(prices)
        width = int(stretch//5)
        
        plt.hist(prices, bins = width)
        plt.show()

    def earliest_date(self):
        """
        Return the date of the earliest sold item collected
        """
        
        if len(self.itemList) == 0:
            return []
        else:
            return self.itemList[-1].date

    def list_from_date_to_today(self, date):
        """
        Return the part of the item list that has items that are more into the future and equal to this date.
        """

        for i in range(len(self.itemList)):
            item = self.itemList[i]

            if item.getDate() >= date:
                return self.itemList[i:]
        else:
            return []

    def new_export(self, exportFile, importList):

        importList.importData(exportFile)

        #add new items from self.itemList to importList.itemList
        earliest_newly_collected_date = self.earliest_date()
        overlapping_list = importList.list_from_date_to_today( earliest_newly_collected_date )
        for item_one in self.itemList:
            member = any([item_one == item_two for item_two in overlapping_list])
            if not member:
                importList.addItem(item_one)

        #sort the list before exporting
        importList.date_sort()

        #export item data to exportFile
        with open(exportFile, "w", encoding = "utf-8") as ebay_csv:
            data = ["title", "price", "date"]
            csv_writer = csv.DictWriter(ebay_csv, fieldnames = data)
            csv_writer.writeheader()

            for item in importList.itemList:
                csv_writer.writerow( item.get_dict_data() )

    def __str__(self):
        string = ""
        for item in self.itemList:
            string += f"{item.getTitle():<100}{item.getPrice():<20}{item.getDate()}\n"

        return string