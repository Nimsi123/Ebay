import datetime

#functions to adjust html inputs to work with my algorithms
def cleanTitle(entry):

    if len(entry) != 1:
        print("entry: ", entry)
        return entry[1]
    else:
        return entry[0]

    #remove all symbols that do not belong

def stripComma(string):
    finalPrice = ""
    for i in string:
        if i != ",":
            finalPrice += i
    return finalPrice

def cleanPrice(entry):
    #print(f"prices before cleaning: {price} prices after cleaning: {price[0].strip()[1:]}")
    if len(entry) == 1:
        price = entry[0]
        if price.find(",") != -1:
            #there is a comma!
            price = stripComma(price)
        return round(float(price.strip()[1:]), 2)
    else:
        return -1

def cleanShipping(entry):

    if type(entry) == list:
        entry = entry[0]

    if entry == "Free shipping" or entry == "Shipping not specified" or entry == "Freight":
        return 0
    elif entry.find("$") == -1:
        #just another safety precaution
        return 0
    else:
        #print("cleaned shipping: ", repr(entry.strip()[2:len(entry)-9]))
        return round(float(entry.strip()[2:len(entry)-9]), 2)

def cleanDate(entry):

    if entry == "nothing found" or entry == "SPONSORED":
        return "nothing found"

    date = entry[len("Sold  "):]

    endMonth = date.find(" ")
    month = date[:endMonth]

    endDay = date.find(", ")
    day = date[endMonth +1:endDay]

    year = date[endDay + len(", "):]

    stringDate = ""
    if month.upper() == "APR":
        month = 4
    elif month.upper() == "MAY":
        month = 5
    elif month.upper() == "JUN":
        month = 6
    elif month.upper() == "JUL":
        month = 7

    #turn date into two digits, if necessary
    #if int(day) < 10:
        #day = "0" + day

    return datetime.datetime(int(year), int(month), int(day))