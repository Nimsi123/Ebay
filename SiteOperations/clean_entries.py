import datetime
import bs4

"""Clean functions return a list to signal a bad input."""

def clean_title(entry):
    """Cleans the title entry.

    :param entry: The title
    :type entry: str
    :returns: The cleaned title
    :rtype: str
    """
    if entry == None:
        return []

    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    return entry

def clean_price(entry):
    """Cleans the price entry.
    
    :param entry: The price entry string.
    :type entry: str
    :returns: The price. Otherwise, returns None if bad entry.
    :rtype: float

    >>> clean_price("$100,000")
    100000
    >>> clean_price("100") #returns None
    >>>
    """
    if entry == None:
        return []

    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    if entry.find("$") != -1:
        try:
            return round(float(entry.replace(',', '').strip()[1:]), 2)
        except:
            #print("bad price: ", entry)
            return [entry]
    else:
        #print("bad price: ", entry)
        return [entry]

def clean_shipping(entry):
    """Cleans the shipping entry.

    :param entry: The shipping entry string.
    :type entry: str
    :returns: The shipping. Otherwise, returns [entry] if bad entry.
    :rtype: float
    """
    if entry == None:
        return []

    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))
    print("shipping entry: ", entry)

    if entry in ["Free shipping", "Shipping not specified", "Freight"] or entry.find("$") == -1 or entry == "":
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
            return [entry]

def clean_date(entry):
    """Cleans the date entry.

    :param entry: The date entry.
    :type entry: str
    :returns: A ``datetime`` object representing the date sold. Otherwise, returns None if bad entry.
    :rtype: ``datetime``
    """
    if entry == None:
        return []
        
    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    if entry.find("Sold") == -1:
        #print("bad date: ", entry)
        return [entry]

    date = entry[len("Sold  "):]

    endMonth = date.find(" ")
    month = date[:endMonth]

    endDay = date.find(", ")
    day = date[endMonth +1:endDay]

    year = date[endDay + len(", "):]

    month_dict = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12
    }

    return datetime.datetime(int(year), month_dict[month.upper()], int(day))
