import bs4

from Ebay.SiteOperations.clean_entries import clean_title, clean_price, clean_shipping, clean_date
from Ebay.ItemOrganization.Item import Item
from Ebay.SiteOperations import printer
from Ebay.SiteOperations.timer import timer

def find_element(html, element_type, attr_key, attr_value):
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

    for element in html.find_all(element_type):
        if element.get(attr_key) == None:
            continue
        else:
            class_name = (element.get(attr_key))[0]

        if class_name.find(attr_value) != -1 and element.contents != None:
            return element

    return None

def find_letters(html, element_type, class_code):
    """Returns a string of letters. All letters are in an html block of 'element_type' with 'class_code.'

    Why?
        --> class_code is used to encrypt the letters that make up the sale date string

    Should return something like "Sold Jun 11, 2020"
    """

    saleDate = ""
    for element in html.find_all(element_type):
        if element.get("class") == None:
            continue
        else:
            class_name = (element.get("class"))[0]

        if class_name.find(class_code) != -1 and element.contents != None:
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

def find_class_name(html, element_type, content):
    """
    in the 'html' code, there is an element of 'element_type' which has 'content'
    if the 'content' matches the element's .contents, then return the class name 'class_name'

    Why?
        --> helper method to find_key

    this 'class_name' is what ebay generated for every letter in the date
    content is one letter in "Sold". we want to find the class_name that is common to all letters in "Sold"
    """

    for element in html.find_all(element_type):
        if element.get("class") == None:
            continue
        else:
            class_name = (element.get("class"))[0]

        if len(element.contents) == 0:
            continue
        
        if element.contents[0] == content:
            #the class name is the KEY
            return class_name

    return None

def find_key(html, element_type, sequence):
    """
    Returns the class name, or 'key', common to all sub elements in 'tag_block.'

    Why?
        --> ebay changed the class_name of the element representing the sale date
    """

    for listing in html.find_all(element_type):
        tagBlock = find_element(listing, "div", "class", "s-item__title--tagblock")

        if tagBlock == None:
            continue

        tagBlock = tagBlock.contents[0]

        keys = []
        for letter in sequence:
            keys.append( find_class_name(tagBlock, "span", letter) )

        if len(set(keys)) == 1:
            #all the keys are identical
            if keys[0] != None:
                return keys[0]

def get_listings_iteration(html):
    """Returns the total number of listings for the query and the number of page iterations.

    :param html: the webpage's entire html
    :type html: 
    :returns: Returns the total number of listings for the query and the number of page iterations.
    :rtype: tuple
    """
    strip_comma = lambda entry: entry.replace(',', '')
    temp_num = extract(find_element, html, "h1", "srp-controls__count-heading", strip_comma)
    
    try:
        total_listings = int(temp_num)
    except Exception as e:
        print(f"Cannot find total listings")
        print("{0:30}: {1}\n".format("extract", temp_num))
        print(e)
        import sys
        sys.exit()
    
    total_listings = int(temp_num)

    if total_listings == 0:
        return None, None

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

def extract(get_raw_func, html, element_type, class_name, clean_func):
    """
    html -> a block of code representing a single listing

    Search the html block for the attribute of an item defined by 'element_type' and 'class_name.'
    Return the result of calling 'clean_func' on the item's attribute.
    """

    raw = get_raw_func(html, element_type, "class", class_name)
    
    if raw == None:
        return None

    while type(raw) == bs4.Tag:
        #go deeper in a nest
        raw = raw.contents[0]

    return clean_func(str(raw)) #usable format for my algorithm

def extract_nested(get_raw_func, html, outer_element_type, outer_class_name, inner_element_type, inner_class_name, clean_func):
    """
    Some attributes are nested within two blocks.
    Returns the attribute accessed by diving into one block, and then going deeper.
    """

    outer_block = find_element(html, outer_element_type, "class", outer_class_name)

    if outer_block == None:
        return None
    
    outer_block = outer_block.contents[0]
    cleaned_inner = extract(get_raw_func, outer_block, inner_element_type, inner_class_name, clean_func)

    return cleaned_inner

def is_overlapping(date_stored, date_appended):
    if (date_stored and date_appended) and (date_appended < date_stored):
        printer.overlap(date_appended, date_stored)
        return True

@timer
def search_listings(html, element_type, class_code, item_collection, printer_bool_page_stats = False):
    """
    html -> html code for an entire webpage

    Adds new items to item_collection.
    """

    #ebay tries to mess with the sale date and my code
    #right before the code starts, I will find the special class_name that can be used to find the sale date!
    key = find_key(html, element_type, ["S", "o", "l", "d"])

    count_added, count_skipped_early, count_skipped_bad, count_skipped_class_code = 0, 0, 0, 0

    for listing in html.find_all(element_type):
        if listing.get("class") == None:
            count_skipped_early += 1
            continue
        else:
            class_name = listing.get("class")[0]

        if class_name == class_code:
            #extract data from a single listing

            title = extract(find_element, listing, "h3", "s-item__title", clean_title)
            price = extract(find_element, listing, "span", "s-item__price", clean_price)
            shipping = extract(find_element, listing, "span", "s-item__shipping", clean_shipping)

            if key == None:
                date = extract(find_element, listing, "div", "s-item__title--tagblock", clean_date)
            else:
                print("*****need to do extra work to get sale date********MANDOLORIAN")
                date = extract_nested(find_letters, listing, "div", "s-item__title--tagblock", "span", key, clean_date)

            if all([attr is not None for attr in [title, price, date, shipping]]):
                total_cost = round(price+shipping, 2)
                item_collection.addItem( Item(title, total_cost, date) )
                count_added += 1
            else:
                #print(f"BAD LISTING -- title: {title} price: {price} shipping: {shipping} date: {date}")
                count_skipped_bad += 1

        else:
            count_skipped_class_code += 1

    if printer_bool_page_stats:
        printer.page_stats_one(len(html.find_all(element_type)), count_added, count_skipped_early, count_skipped_bad, count_skipped_class_code)

