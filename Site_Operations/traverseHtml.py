#findElement
#findAllLetters
#findclass_name
#findKey
#findLink

import time
import functools

globalTimeTotal = 0
globalTimeCounter = 0

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        global globalTimeTotal, globalTimeCounter
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic

        globalTimeTotal += elapsed_time
        globalTimeCounter += 1
        print("average elapsed time: ", globalTimeTotal/globalTimeCounter)
        #print(f"Elapsed time: {elapsed_time:0.8f} seconds")
        return value
    return wrapper_timer

def findElement(html, element_type, attributeKey, attributeValue):
    """
    Returns the FIRST element found with the particular class code in the html code block.
    """

    for element in html.find_all(element_type):
        if element.get(attributeKey) == None:
            continue
        else:
            class_name = (element.get(attributeKey))[0]

        if class_name.find(attributeValue) != -1 and element.contents != None:
            return element

    return "nothing found"

def findAllLetters(html, element_type, class_code):
    """
    Returns a string of letters. All letters are in an html block of 'element_type' with 'class_code.'

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
                    return "nothing found"
                else:
                    return saleDate

    return saleDate

def findclass_name(html, element_type, content):
    """
    in the 'html' code, there is an element of 'element_type' which has 'content'
    if the 'content' matches the element's .contents, then return the class name 'class_name'

    Why?
        --> helper method to findKey

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

    return "nothing found"

def findKey(html, element_type, sequence):
    """
    Returns the class name, or 'key', common to all sub elements in 'tag_block.'

    Why?
        --> ebay changed the class_name of the element representing the sale date
    """

    for listing in html.find_all(element_type):
        tagBlock = findElement(listing, "div", "class", "s-item__title--tagblock")

        if tagBlock == "nothing found":
            continue

        tagBlock = tagBlock.contents[0]

        keys = []
        for letter in sequence:
            keys.append( findclass_name(tagBlock, "span", letter) )

        if len(set(keys)) == 1:
            #all the keys are identical
            if keys[0] != "nothing found":
                return keys[0]

def findLink_new(old_link):
    """
    Given an old link to an eBay page, returns a link to the next page.
    """

    if old_link.find("&_pgn=") == -1:
        return old_link + "&_pgn=2"
    else:
        end = old_link.find("&_pgn=") + len("&_pgn=")
        return old_link[:end] + str((int(old_link[end:]) + 1))

"""
def findLink(html, element_type, class_code):

    element = findElement(html, element_type, "class", class_code)

    if element == "nothing found":
        return "nothing found"
    else:
        return element.get("href")

def countListings(html, element_type, class_code):
    listings = html.find_all(element_type)
    
    count = 0

    for listing in listings:
        try:
            name = (listing.get("class"))[0]
        except:
            continue

        if name == class_code:
            count += 1

    return count
"""