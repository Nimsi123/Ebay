import bs4
import pandas as pd

from eBayScraper.SiteOperations.clean_entries import strip_comma, clean_title, clean_price, clean_shipping, clean_date, NOT_FOUND
from eBayScraper.SiteOperations import printer
from eBayScraper.ItemOrganization.timer import timer
from eBayScraper.data_files.directories import BAD_LISTING_DIR

"""
There is no need for extract nested! Just dive as deep as you want for the nested expression.

>>> x = BeautifulSoup("<div class = 'foo shoo' id = 'bar'></div>")
>>> x.find_all("div", attrs={"class": "foo"})
[<div class="foo shoo" id="bar"></div>]
"""

# TODO: replace all calls to find_element with the bs4 method .find! it does pretty much the exact same thing!
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
    """Returns a string of letters. All letters are in an html block of 'element_type' with 'class_code.'
    Why?
        --> class_code is used to encrypt the letters that make up the sale date string
    Should return something like "Sold Jun 11, 2020"
    """

    saleDate = ""
    for element in html.find_all(element_type, attrs = attrs):
        if element.contents != None:
            try:
                #add another letter to the string
                saleDate += element.contents[0]

            except:
                #code enters this block if element.contents[0] fails
                #   this means we have come to an end of all the letters and we much reach a verdict: either we got the right letters, or we didn't
                if saleDate.find("Sold") == -1:
                    return None
                else:
                    return saleDate

    return saleDate

def find_class_names(html, element_type, content):
    """
    in the 'html' code, there are elements of 'element_type' that has 'content'
    return the class names of all elements for which 'content' matches the element's .contents
    Why?
        --> helper method to find_key
    this 'class_name' is what ebay generated for every letter in the date
    content is one letter in "Sold". we want to find the class_name that is common to all letters in "Sold"
    """

    class_names = []
    for element in html.find_all(element_type):
        if element.get("class") == None:
            continue
        else:
            class_name = element.get("class")[0]

        if len(element.contents) == 0:
            continue

        if element.contents[0] == content:
            #the class name is the KEY
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

    return max(set(keys), key = keys.count)

    """
    keys = [key for key in keys if key != None]
    print("keys: ", keys)


    if len(set(keys)) == 1:
        #all the keys are identical
        if keys[0] != None:
            return keys[0]
    print("nothing matching")
    return None
    """

def get_listings_iteration(html):
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

    # 4/1/21 this try except block is unnecessary. just find total_listings = int(temp_num)
    try:
        total_listings = int(temp_num)
    except Exception as e:
        print(f"Cannot find total listings")
        print("{0:30}: {1}\n".format("extract", temp_num))
        raise e
        #return None, None

    #ebay won't show us more that 10,000 items from their page even though there might be more to look at
    max_iteration = min(50, int(total_listings/200 +1))

    return total_listings, max_iteration

def next_link(old_link):
    """Given an old link to an eBay page, returns a link to the next page.

    :param old_link: The previous link
    :type old_link: str
    :returns: The next link.
    :rtype: str
    """

    if old_link.find("&_pgn=") == -1:
        return old_link + "&_pgn=2"
    else:
        end = old_link.find("&_pgn=") + len("&_pgn=")
        return old_link[:end] + str((int(old_link[end:]) + 1))

'''
def get_subelement(html, outer_spec):

    """
    Follows the specifications of outer_spec down the tree. Returns the FIRST html tag that is a found down the tree.
    >>> html = BeautifulSoup("<span class = 'out'><div class = 'in2'></div><div class = 'in'><div><div></div></div></div></span>", "html.parser")
    >>> get_subelement(html, [("span", "out"), ("div", "in")])
    <div class="in"><div><div></div></div></div>
    """

    if len(outer_spec) == 0:
        return html

    element_type, class_name = outer_spec[0]
    elements = html.find_all(element_type, class_ = class_name)

    for element in elements:
        sub_elem = get_subelement(element, outer_spec[1:])
        if sub_elem:
            return sub_elem

    return None
'''


def get_subelement(html, outer_spec):
    """
    >>> html = BeautifulSoup("<span class = 'out'><div class = 'in'></div></span>", "html.parser")
    >>> get_subelement(html, [("span", "out")])
    <div class="in"></div>

    >>> html = BeautifulSoup("<span class = 'out'><div class = 'in2'></div><div class = 'in'></div></span>", "html.parser")
    >>> get_subelement(html, [("span", "out")])
    <div class="in2"></div>

    """

    outer_block = html
    for outer_element_type, outer_class_name in outer_spec:
        outer_block = find_element(outer_block, outer_element_type, {"class": outer_class_name})

        if outer_block == None:
            return None
        else:
            outer_block = outer_block.contents[0]
    return outer_block

def extract_nested(find, html, outer_spec, inner_element_type, inner_class_name, clean_func):
    """
    Some attributes are nested within two blocks.
    Returns the attribute accessed by diving into one block, and then going deeper.
    """

    outer_block = get_subelement(html, outer_spec)

    if outer_block == None:
        return None

    cleaned_inner = extract(outer_block, inner_element_type, inner_class_name, clean_func, find = find)

    return cleaned_inner

def extract(html, element_type, class_name, clean_func, find = find_element):
    """ Searches ``html`` for the contents of the first html tag of ``element_type`` and ``class_name``. 
    Before returning the html contents, clean the value with the ``clean_func``.
    
    :param html: a block of code representing a single listing
    :type html:
    :param element_type: The element type of the html tag to search for. For example, ``div``.
    :type element_type: str
    :param class_name: The class name of the html tag to search for.
    :type class_name: str
    :param clean_func: The function that converts the web text into a usable, readable format in the underlying data structure.
    :type clean_func: function
    :returns: The return value of clean_func on the inner contents on the found html tag.
    Passes None to clean_func if nothing is found.
    :rtype: Ranges from str to int to datetime.datetime. 
    """

    raw = find(html, element_type, {"class": class_name})
    
    if raw == None:
        return clean_func(None)

    while type(raw) == bs4.Tag:
        #go deeper in a nest
        raw = raw.contents[0]

    return clean_func(str(raw)) #usable format for my algorithm

def is_overlapping(date_stored, date_appended):
    """Determines whether date_stored is more into the past than date_appended. That is, date_appended is closer to the present day.

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
        # we use extract_nested in case there might be other elements like <span class = '{key}'></span> within listing,
        # but outside of <div class = "s-item__title--tagblock"></div>
        date = extract_nested(find_letters, listing, [("div", "s-item__title--tagblock")], "span", key, clean_date)

    return title, price, shipping, date

def good_data(*data):
    return all([type(attr) is not list for attr in data])

def search_listings(html, key, print_stats = False):
    """Yields item data from listings in a single page's html.
    
    :param html: html code for an entire webpage
    :type html:
    :param print_stats: Determines whether to print updates on the scraping process
    :type print_stats: bool
    :yields: the title, total_cost and date associated with a single listing on the html page.
    """
    element_type, class_code = "li", "s-item"
    bad_listing_store = pd.read_csv(BAD_LISTING_DIR)

    counter = dict([("added", 0), ("skipped_early", 0), ("class_code", 0), ("bad", 0)])

    for listing in html.find_all(element_type, class_ = class_code):
        title, price, shipping, date = get_data(listing, key)

        if good_data(title, price, date, shipping):
            total_cost = round(price+shipping, 2)
            yield title, total_cost, date
            counter["added"] += 1
        else:
            title, price, date, shipping = [item[0] if type(item) == list else item for item in [title, price, date, shipping]]
            bad_listing_store = bad_listing_store.append({
                "title": title,
                "price": price,
                "shipping": shipping,
                "date": date
                }, ignore_index=True)

            counter["bad"] += 1

    bad_listing_store.drop_duplicates().to_csv(BAD_LISTING_DIR, index = None)

    if print_stats:
        num_listings = len(html.find_all(element_type))
        printer.page_stats_one(num_listings, **counter)
