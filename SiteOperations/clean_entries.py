from datetime import datetime
import bs4

"""Clean functions return a list with a single element to signal a bad input.
This can be the NOT_FOUND element, or a custom list with the bad string as the first and only element."""
NOT_FOUND = ["element not found in html"]

strip_comma = lambda entry: NOT_FOUND if entry == None else entry.replace(',', '')

def clean_title(entry):
    """Cleans the title entry.

    :param entry: The title
    :type entry: str
    :returns: The cleaned title
    :rtype: str
    """
    if entry == None:
        return NOT_FOUND

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
        return NOT_FOUND

    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    if entry.find("$") != -1:
        try:
            return round(float(entry.replace(',', '').strip()[1:]), 2)
        except:
            return [entry]
    else:
        return [entry]

def clean_shipping(entry):
    """Cleans the shipping entry.

    :param entry: The shipping entry string.
    :type entry: str
    :returns: The shipping. Otherwise, returns [entry] if bad entry.
    :rtype: float
    """
    if entry == None:
        return NOT_FOUND

    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    def zero_for_shipping(entry):
        """Determines if we should set shipping to zero."""
        return entry in ["Free shipping", "Shipping not specified", "Freight"] \
                or entry.find("$") == -1 or entry == ""

    if zero_for_shipping(entry):
        return 0
    else:
        try:
            message = entry.replace(',', '').strip()[2:len(entry)-9]
            if "shipping" in message: #both cases occur frequently
                return round(float(message[:-9]))
            else:
                return round(float(message), 2)
        except:
            return [entry]

def clean_date(entry):
    """Cleans the date entry.

    :param entry: The date entry.
    :type entry: str
    :returns: A ``datetime`` object representing the date sold. Otherwise, returns None if bad entry.
    :rtype: ``datetime``
    """
    if entry == None:
        return NOT_FOUND

    assert type(entry) == str, "entry is of type {}, not str".format(type(entry))

    if entry.find("Sold") == -1:
        return [entry]

    date_str = entry[len("Sold  "):]
    return datetime.strptime(date_str, "%b %d, %Y")