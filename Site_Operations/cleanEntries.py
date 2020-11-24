import datetime
import bs4

#functions to adjust html inputs to work with my algorithms
def clean_title(entry):
    return entry

def strip_comma(num_string):
    """
    >>> strip_comma("100,000")
    '100000'
    """

    return num_string.replace(',', '')

def clean_price(entry):
    """
    >>> clean_price("$100,000")
    100000
    >>> clean_price("100") #returns None
    >>>
    """

    if entry.find("$") != -1:
        try:
            return round(float(entry.replace(',', '').strip()[1:]), 2)
        except:
            print("entry: ", entry)
            print("bad price")
            return None
    else:
        return None

def clean_shipping(entry):

    """
    if type(entry) == list:
        print("is this ever a case?")
        entry = entry[0]
    """

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
            print("bad shipping: ", entry)
            return None

def clean_date(entry):
    """
    Outputs a datetime object representing the date sold.
    """

    """
    #coerce entry into a string
    if type(entry) == bs4.Tag:
        print("needed to take the extra step again in clean_date")
        entry = str(entry.contents[0])
    elif type(entry) == str:
        pass
    else:
        print(f"entry type: {type(entry)}")
        print("date not able to become a string")
        return None
    """

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