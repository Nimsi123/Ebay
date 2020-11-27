import datetime
import bs4

#functions to adjust html inputs to work with my algorithms
def clean_title(entry):
    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    return entry

def clean_price(entry):
    """
    >>> clean_price("$100,000")
    100000
    >>> clean_price("100") #returns None
    >>>
    """
    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    if entry.find("$") != -1:
        try:
            return round(float(entry.replace(',', '').strip()[1:]), 2)
        except:
            #print("bad price: ", entry)
            return None
    else:
        return None

def clean_shipping(entry):
    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    if entry in ["Free shipping", "Shipping not specified", "Freight"] or entry.find("$") == -1:
        return 0
    else:
        try:
            message = entry.replace(',', '').strip()[2:len(entry)-9]
            if "shipping" in message:
                return round(float(message[:-9]))
            else:
                return round(float(message), 2)
        except:
            #print("bad shipping: ", entry)
            return None

def clean_date(entry):
    """
    Outputs a datetime object representing the date sold.
    """
    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    if entry.find("Sold") == -1:
        #print("bad date: ", entry)
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