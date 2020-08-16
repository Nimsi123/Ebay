import datetime

#functions to adjust html inputs to work with my algorithms
def cleanTitle(entry):
    return entry

def stripComma(string):
    finalPrice = ""
    for i in string:
        if i != ",":
            finalPrice += i
    return finalPrice

def cleanPrice(entry):

    if entry.find("$") != 0:
        return None

    if entry.find(",") != -1:
        #there is a comma!
        entry = stripComma(entry)

    return round(float(entry.strip()[1:]), 2)

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
        return round(float(stripComma(entry.strip()[2:len(entry)-9])), 2)

def cleanDate(entry):
    try:
        entry = entry.contents
    except:
        pass
    try:
        entry = entry[0]
    except:
        pass

    try:
        entry = str(entry)
    except:
        print("date not able to become a string")

    if entry.find("Sold") == -1:
        return None

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
    elif month.upper() == "AUG":
        month = 8

    return datetime.datetime(int(year), int(month), int(day))