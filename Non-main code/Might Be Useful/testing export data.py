storedData = [4, 3, 2, 1]

newData = [7, 6, 5]
newData = [0, -1, -2]
newData = [4, 3, 2, 1]


def getStoredLatestDate(exportFile):
    return exportFile[-1]

def getStoredEarliestDate(exportFile):
    return exportFile[0]

def overlapDateMarkerA(itemList, oldFile):
    #if there is an overlap in the start of the oldfile, return the index that is the FIRST to enter the overlap zone

    markerA = getStoredEarliestDate(oldFile)
    for item in itemList:
        if item < markerA:
            #does an item in self.itemList go farther in the past than markerA?
            return itemList.index(item)
    else:
        return -1

def overlapDateMarkerB(itemList, oldFile, indexEarlierThanA):
    #if there is an overlap in the start of the oldfile, return the index that is the FIRST to enter the overlap zone

        markerB = getStoredLatestDate(oldFile)
        for item in itemList[indexEarlierThanA:]:
            if item < markerB:
                #does an item in self.itemList go farther in the past than than markerB?
                return itemList.index(item)
        else:
            return -1

def overlap(itemList, oldFile):

    overlapA = overlapDateMarkerA(itemList, oldFile)
    if overlapA == -1:
        #nothing goes farther than markerA into the past
        #everything is more into the future, and it will not go far enough in the past to overlap with before

        #export data starting at the beginning of the file

        #END THE EXPORT
        #export to the start of the file, from [0:len(list)]
        return [[0, len(itemList)], -1]
    else:
        #at some point, self.itemList does bleed into existing data territory
        #do not go PAST marker A

        #export data starting at the beginning of the file for self.itemList[:overlapA]

        #if data goes past markerB, then print that. if nothing goes past markerB, we are done and there is nothing new to submit
        overlapB = overlapDateMarkerB(itemList, oldFile, overlapA)

        if overlapB == -1:
            #doesn't go past markerB
            return [[[0, overlapA-1], -1]]
        else:
            #export data after marker B self.itemList[overlapB:]
            return [[0, overlapA], [overlapB, len(itemList)]]

print(overlap(newData, storedData))