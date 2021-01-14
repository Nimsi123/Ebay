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