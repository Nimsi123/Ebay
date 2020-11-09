import matplotlib.pyplot as plt
import statistics
import csv
import datetime
import statistics

#from MonthlyReport import MonthlyReport


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

    def getStoredLatestDate(exportFile):
        with open(exportFile, "r", encoding = "utf-8") as ebay_csv:
            csv_reader = csv.DictReader(ebay_csv)
            endDate = 0
            for line in csv_reader:
                endDate = line["date"]
                #this is the date that is into the past!
            return datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]))

    def getStoredEarliestDate(exportFile):
        with open(exportFile, "r", encoding = "utf-8") as ebay_csv:
            csv_reader = csv.DictReader(ebay_csv)
            for line in csv_reader:
                endDate = line["date"]
                #this is the date that is into the past!
                return datetime.datetime(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:10]))

    def overlapDateMarkerA(self, oldFile):
        #if there is an overlap in the start of the oldfile, return the index that is the FIRST to enter the overlap zone

        markerA = ItemList.getStoredEarliestDate(oldFile)
        for item in self.itemList:
            #print("item detail: ", item.getTitle(), item.getPrice(), item.getDate())
            if item.getDate() <= markerA:
                #print("ENTER****************************************")
                #print("dates: ", item.getDate(), markerA)
                #print("item detail: ", item.getTitle(), item.getPrice(), item.getDate())
                #does an item in self.itemList go farther in the past than markerA?
                return self.itemList.index(item)
        else:
            return -1

    def overlapDateMarkerB(self, oldFile, indexEarlierThanA):
        #if there is an overlap in the end of the oldfile, return the index that is the LAST in the overlap

        #this should be reversed
        markerB = ItemList.getStoredLatestDate(oldFile)
        for item in self.itemList[indexEarlierThanA:]:
            if item.getDate() < markerB:
                #does an item in self.itemList go farther in the past than than markerB?
                return self.itemList.index(item)
        else:
            return -1

    def overlap(self, oldFile):
        lines_in_file = open(oldFile, 'r', encoding = "utf-8").readlines()
        number_of_lines = len(lines_in_file)

        #print(lines_in_file)
        #print("number: ", number_of_lines)

        if number_of_lines == 0:
            #no overlap
            #print("no overlap")
            #print("lines: ", lines_in_file)
            return [False, [0, len(self.itemList)], -1]
        else:
            overlapA = self.overlapDateMarkerA(oldFile)
            if overlapA == -1:
                #nothing goes farther than markerA into the past
                #everything is more into the future, and it will not go far enough in the past to overlap with before

                #export data starting at the beginning of the file

                #END THE EXPORT
                #export to the start of the file, from [0:len(list)]
                return [True, [0, len(self.itemList)], -1]
            else:
                #at some point, self.itemList does bleed into existing data territory
                #do not go PAST marker A

                #export data starting at the beginning of the file for self.itemList[:overlapA]

                #if data goes past markerB, then print that. if nothing goes past markerB, we are done and there is nothing new to submit
                overlapB = self.overlapDateMarkerB(oldFile, overlapA)

                if overlapB == -1:
                    #doesn't go past markerB
                    return [True, [0, overlapA], -1]
                else:
                    #export data after marker B self.itemList[overlapB:]
                    return [True, [0, overlapA], [overlapB, len(self.itemList)]]





    def exportData(self, exportFile):

        package = self.overlap(exportFile)
        print("package: ", package)
        if package[0] == False:
            
            #there is no previous data in the file
            #it is initially empty
            #write header
            with open(exportFile, "w", encoding = "utf-8") as ebay_csv:
                data = ["title", "price", "date"]
                csv_writer = csv.DictWriter(ebay_csv, fieldnames = data)
                #print("writing header")
                csv_writer.writeheader()
                for item in self.itemList:
                    csv_writer.writerow({"title": item.getTitle(), "price": item.getPrice(), "date": item.getDate()})
            return
        #print("dumping")

        if package[1] == -1:
            return
        else:
            self.prepend_dump(exportFile, package[1])

        if package[2] == -1:
            return
        else:
            self.append_dump(exportFile, package[2])
        #print("passed dump")

    def appendFileToFile(oldFile, tempFileName, needsHeader):
        with open(tempFileName, "a", encoding = "utf-8") as ebay_csv_temp:
            data = ["title", "price", "date"]
            csv_writer = csv.DictWriter(ebay_csv_temp, fieldnames = data)

            with open(oldFile, "r", encoding = "utf-8") as ebay_csv:
                csv_reader = csv.DictReader(ebay_csv)

                if needsHeader:
                    csv_writer.writeheader()

                for line in csv_reader:
                    csv_writer.writerow({"title": line["title"], "price": line["price"], "date": line["date"]})


    def prepend_dump(self, exportFile, indexRange):
        ########this step is inefficient
        with open("temp.csv", "w") as file:
            file.truncate()
            pass
        #i want to truncate this file

        ItemList.appendFileToFile(exportFile, "temp.csv", True)

        with open(exportFile, "w", encoding = "utf-8") as ebay_csv:

            data = ["title", "price", "date"]
            csv_writer = csv.DictWriter(ebay_csv, fieldnames = data)
            csv_writer.writeheader()
            for item in self.itemList[indexRange[0]: indexRange[1]]:
                csv_writer.writerow({"title": item.getTitle(), "price": item.getPrice(), "date": item.getDate()})

        ItemList.appendFileToFile("temp.csv", exportFile, False)

    def append_dump(self, exportFile, indexRange):

        with open(exportFile, "a", encoding = "utf-8") as ebay_csv:

            data = ["title", "price", "date"]
            csv_writer = csv.DictWriter(ebay_csv, fieldnames = data)

            for item in self.itemList[indexRange[0]: indexRange[1]]:
                csv_writer.writerow({"title": item.getTitle(), "price": item.getPrice(), "date": item.getDate()})