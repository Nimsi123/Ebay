import csv
import statistics
import datetime



from Ebay.ItemOrganization.Item import Item

class ProductList:
    def __init__(self):
        self.item_list = []
        self.listOfPrices = []
        self.averagePriceSold = None
        self.percentUnderAverage = None

    def addItem(self, item):
        """
        Add an Item object to item_list
        """
        self.item_list.append(item)

    def date_sort(self):
        """
        Sort the item_list by date. Earliest date in the beginning of the list.
        """

        self.item_list.sort(key = lambda item: item.date)

    def import_item_data(self, dataFile):
        """
        Open up a csv file that holds individual item data. Populate the item_list with newly created Item objects.
        """

        with open(dataFile, "r", encoding = "utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                d = line["date"]
                date = datetime.datetime(int(d[0:4]), int(d[5:7]), int(d[8:10]))
                self.item_list.append( Item(line["title"], float(line["price"]), date ) )

    """EXPORT CODE"""

    def split_data(self):
        """
        Returns three new meaningful lists extracted from self.item_list
        --> (date_list, avg_price_list, volume_list)
        """
        
        if len(self.item_list) == 0:
            return False

        #items grouped by date
        item_dict = {}
        for item in self.item_list:
            item_dict[item.get_date()] = item_dict.get(item.get_date(), []) + [item]

        date_list, avg_price_list, volume_list = [], [], []
        for date, itemSubset in item_dict.items():
            avgPrice = statistics.mean([item.get_price() for item in itemSubset])

            date_list.append(date)
            avg_price_list.append(avgPrice)
            volume_list.append( len(itemSubset) )

        return date_list, avg_price_list, volume_list

    def earliest_date(self):
        """
        Return the date of the earliest sold item collected. Farthest into the past.
        """
        
        if len(self.item_list) == 0:
            return False
        else:
            return self.item_list[-1].date

    def list_from_date_to_today(self, date):
        """
        Return the part of the item list that has items that are more into the future and equal to this date.
        """

        for i in range(len(self.item_list)):
            item = self.item_list[i]

            if item.get_date() >= date:
                return self.item_list[i:]
        else:
            return []

    def file_write(self, export_file):
        """
        Dumps item data from self.item_list into export_file.
        export_file is written over.
        """

        with open(export_file, "w", encoding = "utf-8") as ebay_csv:
            data = ["title", "price", "date"]
            csv_writer = csv.DictWriter(ebay_csv, fieldnames = data)
            csv_writer.writeheader()

            for item in self.item_list:
                csv_writer.writerow( item.get_dict_data() )

    def export_item_data(self, export_file):
        """
        export_list --> the list holding all the items to export
        """

        export_list = ProductList()
        export_list.import_item_data(export_file) #get all old item data already collected

        if len(self.item_list) == 0:
            return False

        earliest_newly_collected_date = self.earliest_date() #Farthest into the past.
        overlapping_list = export_list.list_from_date_to_today( earliest_newly_collected_date )

        #add new items, not existing items
        for item_one in self.item_list:
            if item_one not in overlapping_list:
                export_list.addItem(item_one)

        export_list.date_sort()
        export_list.file_write(export_file)

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
        while i < len(self.item_list):
            if self.item_list[i].get_price() >= topPrice:
                #delete the item with the outlier price
                del self.item_list[i]
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
        for item in self.item_list:
            string += f"{item.get_title():<100}{item.get_price():<20}{item.get_date()}\n"

        string += "\n\n\n"

        string += f"Mean: {self.mean} "
        string += f"Median: {self.median} "
        string += f"Standard Deviation: {self.stdev}"

        return string