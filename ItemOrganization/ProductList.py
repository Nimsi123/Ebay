import csv
import statistics
import datetime



from Ebay.ItemOrganization.Item import Item

class ProductList:
    def __init__(self):
        self.itemList = []
        self.listOfPrices = []
        self.averagePriceSold = None
        self.percentUnderAverage = None

    def addItem(self, item):
        """
        Add an Item object to itemList
        """
        self.itemList.append(item)

    def date_sort(self):
        """
        Sort the itemList by date. Earliest date in the beginning of the list.
        """

        self.itemList.sort(key = lambda item: item.date)

    def importData(self, dataFile):
        """
        Open up a csv file that holds individual item data. Populate the itemList with newly created Item objects.
        """

        with open(dataFile, "r", encoding = "utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                d = line["date"]
                date = datetime.datetime(int(d[0:4]), int(d[5:7]), int(d[8:10]))
                self.itemList.append( Item(line["title"], float(line["price"]), date ) )

    """EXPORT CODE"""

    def splitData(self):
        """
        self.itemList is a list of items.
        extract three new meaningful lists from self.itemList
        --> (dateList, avgPriceList, volumeList)
        """

        #key:value
        #date (mm/dd/yyyy): list of items
        reportDictionary = {}

        #put all the sales in a dictionary
        if len(self.itemList) == 0:
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
        reportAverageDictionary = {}
        #date: total sales on this date
        reportVolumeDictionary = {}

        dateList = []
        avgPriceList = []
        volumeList = []
        #for every date, organize the average price and volume of sales
        for date, itemSubset in reportDictionary.items():
            avgPrice = statistics.mean([item.getPrice() for item in itemSubset])

            reportAverageDictionary[date] = avgPrice
            reportVolumeDictionary[date] = len(itemSubset)

            #make lists for plotting
            dateList.append(date)
            avgPriceList.append(avgPrice)
            volumeList.append( len(itemSubset) )

        return (dateList, avgPriceList, volumeList)

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

    """DATA ANALYSIS CODE"""

    def make_stats(self):
        self.mean = round(statistics.mean(self.listOfPrices), 2)
        self.median = round(statistics.median(self.listOfPrices), 2)
        self.stdev = round(statistics.stdev(self.listOfPrices), 2)

    def plotHistogram(self):
        prices = self.getListOfPrices()
        stretch = max(prices) - min(prices)
        width = int(stretch//5)
        
        plt.hist(prices, bins = width)
        plt.show()

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

    def __str__(self):
        string = ""
        for item in self.itemList:
            string += f"{item.getTitle():<100}{item.getPrice():<20}{item.getDate()}\n"

        string += "\n\n\n"

        string += f"Mean: {self.mean} "
        string += f"Median: {self.median} "
        string += f"Standard Deviation: {self.stdev}"

        return string