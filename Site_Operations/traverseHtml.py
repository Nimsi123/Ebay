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
    #given HTML code, return the FIRST element found with the particular class code

    for element in html.find_all(element_type):
        #print("element: ", element)
        if element.get(attributeKey) == None:
            continue
        else:
            class_name = (element.get(attributeKey))[0]
            #print("class_name: ", class_name)

        #html handles classes weirdly
        #an element can have its classes separated by spaces
        #print("attribute: ", attributeKey, attributeValue)
        #print("class name: ", class_name, "--", attributeValue)
        #print("truths: ", class_name.find(attributeValue), element.contents != None)
        if class_name.find(attributeValue) != -1 and element.contents != None:
            return element

    return "nothing found"

def findAllLetters(html, element_type, class_code):
    #a modified version of findElement

    #class_code is used to encrypt the letters that make up the sale date string
    #go through all the elements in the html subset with 'element_type'
    #   collect all the elements with the proper 'class_code' meanwhile filtering through the fake letters
    #   at the time of return, the string (ex. "Sold Jun 11, 2020") should be completed


    saleDate = ""
    for element in html.find_all(element_type):
        if element.get("class") == None:
            continue
        else:
            class_name = (element.get("class"))[0]

        #html handles classes weirdly
        #an element can have its classes separated by spaces

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
                    #enters this block if element.contents[0] fails, but the date is complete in string
                    return saleDate

    #print("leaving here")
    #to leave from here means that the for loop completed well
    return saleDate

def findclass_name(html, element_type, content):
    #in the 'html' code, there is an element of 'element_type' which has 'content'
    #if the 'content' matches the element's .contents, then return the class name 'class_name'

    #USES
    #this 'class_name' is what ebay generated for every letter in the date
    #content is one letter in "Sold". we want to find the class_name that is common to all letters in "Sold"

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
    #ebay changed the class_name of the element representing the sale date

    #this function will return the class name common to all of the sub elements in 'tagBlock' -- i regard the common class_name as the "key"

    for listing in html.find_all(element_type):
        tagBlock = findElement(listing, "div", "class", "s-item__title--tagblock")

        if tagBlock == "nothing found":
            #bad listing
            continue
        else:
            tagBlock = tagBlock.contents
        
        keys = []
        for letter in sequence:
            #find a key
            keys.append( findclass_name(tagBlock[0], "span", letter) )

        if len(set(keys)) == 1:
            #all the keys are identical
            
            if keys[0] == "nothing found":
                #print("returning keys none: ")
                return None
            else:
                #print("returning keys: ", keys[0])
                return keys[0]
    else:
        #print("returning keys none: ")
        return None


def findLink(html, element_type, class_code):

    element = findElement(html, element_type, "class", class_code)

    if element == "nothing found":
        return "nothing found"
    else:
        return element.get("href")

def findLink_new(old_link):
    if old_link.find("&_pgn=") == -1:
        return old_link + "&_pgn=2"
    else:
        end = old_link.find("&_pgn=") + len("&_pgn=")
        return old_link[:end] + str((int(old_link[end:]) + 1))

"""
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