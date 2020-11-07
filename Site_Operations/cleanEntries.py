import datetime
import bs4

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
        try:
            message = stripComma(entry.strip()[2:len(entry)-9])
            if "shipping" in message:
                return round(float(message[:-9]))
            else:
                return round(float(message), 2)
        except:
            print("bad shipping: ", entry)
            return None

def cleanDate(entry):

    #coerce entry into a string
    if type(entry) == bs4.Tag:
        entry = str(entry.contents[0])
    else:
        print(f"entry type: {type(entry)}")
        print("date not able to become a string")
        return None

    if entry.find("Sold") == -1:
        return None

    date = entry[len("Sold  "):]

    endMonth = date.find(" ")
    month = date[:endMonth]

    endDay = date.find(", ")
    day = date[endMonth +1:endDay]

    year = date[endDay + len(", "):]

    month_dict = {
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11
    }

    return datetime.datetime(int(year), month_dict[month.upper()], int(day))