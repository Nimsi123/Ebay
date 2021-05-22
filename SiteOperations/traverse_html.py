import bs4
import pandas as pd

from eBayScraper.SiteOperations.clean_entries import strip_comma, clean_title, clean_price, clean_shipping, clean_date, NOT_FOUND
from eBayScraper.SiteOperations import printer
from eBayScraper.ItemOrganization.timer import timer

def find_element(html, element_type, attrs):
    """Returns the FIRST element found in the html code block for which the element's value at attr_key matches the attr_value.

    :param html: The HTML block to search.
    :type html: 
    :param element_type: The HTML tag to search for.
    :type element_type: str
    :param attr_key: The key of an element's attribute.
    :type attr_key: str
    :param attr_val: If the element's value at key equals attr_value, we have our match.
    :type attr_val: str
    :returns: An HTML element within `html` that satisfies the condition. Returns None if an element is not found.
    :rtype: bs4.element.Tag or None
    """

    for element in html.find_all(element_type, attrs = attrs):
        if element.contents != None:
            return element

    return None

def find_letters(html, element_type, attrs):
    """Returns a string of letters. Each letter in the returned string is
    in an html tag of 'element_type' with corresponding attrs.
    Should return something like "Sold Jun 11, 2020".

    :param html: The HTML block to search.
    :type html: 
    :param element_type: The HTML tag type to search for.
    :type element_type: str
    :param attrs: Attributes that the target html tag must have.
    :type attrs: dict
    """

    saleDate = ""
    for element in html.find_all(element_type, attrs = attrs):
        if element.contents == None:
            continue

        try:
            saleDate += element.contents[0]
        except:
            #we have come to an end of all the letters and we much reach a verdict: 
            # either we got the right letters, or we didn't
            if saleDate.find("Sold") == -1:
                return None
            else:
                return saleDate

    return saleDate

def find_class_names(html, element_type, content):
    """Return the class names of all elements for which 'content' matches the element's contents. 
    Helper method to find_key. This 'class_name' is what ebay generated for every letter in the date. 
    We want to find the class_name that is common to all letters in "Sold", for example. 

    :param html: The html block to search
    :type html:
    :param element_type: The html tag type to inspect
    :type element_type: str
    :param content: The content to compare with the content in the html tag.
    :type content: str
    """

    class_names = []
    for element in html.find_all(element_type):
        if element.get("class") == None or len(element.contents) == 0:
            continue
        else:
            class_name = element.get("class")[0]

        if element.contents[0] == content:
            #the contents in the html tag matches what we desire. the class name is a possible KEY
            class_names.append(class_name)

    return class_names

def find_key(html, sequence):
    """
    Returns the class name, or 'key', most commonly seen in all sub elements in 'tag_block' that
    have the letters in sequence.

    Why?
        --> ebay changed the class_name of the element representing the sale date
    """
    assert len(sequence) != 0

    tagBlock = find_element(html, "div", {"class": "s-item__title--tagblock"})

    if not tagBlock:
        return None

    # tag block contains all the <span class="s-jnpuot">S</span> elements.

    keys = []
    for letter in sequence:
        keys.extend(find_class_names(tagBlock, "span", letter))

    if set(keys):
        return max(set(keys), key = keys.count)
    else:
        return None

def get_num_listings_iteration(html):
    """Returns the total number of listings for the query and the number of page iterations.

    :param html: the webpage's entire html
    :type html: 
    :returns: Returns the total number of listings for the query and the number of page iterations.
    :rtype: tuple
    """
    
    temp_num = extract(html, "h1", "srp-controls__count-heading", strip_comma)
    
    if temp_num == NOT_FOUND:
        return NOT_FOUND, NOT_FOUND

    # type of temp_num must be str at this point
    total_listings = int(temp_num)

    # ebay won't show us more that 10,000 items from their page even though there might be more to look at
    max_iteration = min(50, int(total_listings/200 +1))

    return total_listings, max_iteration

def extract(html, element_type, class_name, clean_func, find = find_element):
    """Searches ``html`` for the contents of the first html tag of ``element_type`` and ``class_name``. 
    Before returning the html contents, clean the value with the ``clean_func``. 
    Passes None to clean_func if nothing is found.
    
    :param html: a block of code representing a single listing
    :type html:
    :param element_type: The element type of the html tag to search for. For example, ``div``.
    :type element_type: str
    :param class_name: The class name of the html tag to search for.
    :type class_name: str
    :param clean_func: The function that converts the web text into a usable, readable format in the underlying data structure.
    :type clean_func: function
    :returns: The return value of clean_func on the inner contents on the found html tag.
    :rtype: Ranges from str to int to datetime.datetime. 
    """

    raw = find(html, element_type, {"class": class_name})
    
    if raw == None:
        return clean_func(None)

    while type(raw) == bs4.Tag:
        #go deeper in a nest
        if raw.contents == []:
            return clean_func(None)

        raw = raw.contents[0]

    return clean_func(str(raw)) #usable format for my algorithm

def is_overlapping(date_stored, date_appended):
    """Determines whether date_stored is more into the past than date_appended. 
    That is, date_appended is closer to the present day.

    :param date_stored, date_appended: Dates in time.
    :type date_stored, date_appended: datetime.datetime
    :returns: True if date_appended is closer to present day than date_stored.
    :rtype: bool
    """
    if (date_stored and date_appended) and (date_appended < date_stored):
        printer.overlap(date_appended, date_stored)
        return True

def get_data(listing, key):
    """Returns all meaningfull item data from the html block.

    Takes ~0.001 seconds. Pretty fast. 0.001 * 30,000 listings -> 30 seconds

    :param listing: html block containing item data for a single listing.
    :type listing:
    :returns: the title, price, shipping, and date values of the listing.
    :rtype: tuple
    """

    title = extract(listing, "h3", "s-item__title", clean_title)
    price = extract(listing, "span", "s-item__price", clean_price)
    shipping = extract(listing, "span", "s-item__shipping", clean_shipping)

    if key == None:
        date = extract(listing, "div", "s-item__title--tagblock", clean_date)
    else:
        # in case there might be other elements like <span class = '{key}'></span> within listing,
        # but outside of <div class = "s-item__title--tagblock"></div>
        
        outer_block = find_element(listing, "div", {"class": "s-item__title--tagblock"})

        if outer_block == None:
            date = NOT_FOUND
        else:
            outer_block = outer_block.contents[0]
            date = extract(outer_block, "span", key, clean_date, find_letters)

    return title, price, shipping, date

def good_data(*data):
    return all([type(attr) is not list for attr in data])

def search_listings(html, key, bad_listings, print_stats = False):
    """Returns all item data from listings in a single page's html.
    
    (time measured from function call to return, not each yield time.)
    Improved time from 2.5 - 1.9 seconds by fixing BadListings.add
    Improved time from 1.9 to 0.3 seconds by removing the generator feature. 
    Our data wasn't very memory expensive, so it didn't make sense to use a generator.

    :param html: html code for an entire webpage
    :type html:
    :param print_stats: Determines whether to print updates on the scraping process
    :type print_stats: bool
    :returns: the title, total_cost and date associated with all listings on the html page.
    :rtype: list of lists
    """
    import time
    start = time.time()

    element_type, class_code = "li", "s-item"
    counter = dict([("added", 0), ("skipped_early", 0), ("class_code", 0), ("bad", 0)])
    listing_data = []

    for listing in html.find_all(element_type, class_ = class_code):
        title, price, shipping, date = get_data(listing, key)

        if good_data(title, price, date, shipping):
            total_cost = round(price+shipping, 2)
            #yield title, total_cost, date
            listing_data.append([title, total_cost, date])
            counter["added"] += 1
        else:
            bad_listings.add(
                *[item[0] if type(item) == list else item for item in [title, price, date, shipping]]
            )
            counter["bad"] += 1


    if print_stats:
        num_listings = len(html.find_all(element_type))
        printer.page_stats_one(num_listings, **counter)

    print(time.time() - start, "seconds")
    return listing_data
