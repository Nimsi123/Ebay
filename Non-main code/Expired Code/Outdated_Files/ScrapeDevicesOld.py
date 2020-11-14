from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import webbrowser
import time
import sys
from fpdf import FPDF

from Item import Item
#from Item import ItemList
from Product import ProductList
from cleanEntries import cleanTitle
from cleanEntries import cleanPrice
from cleanEntries import cleanShipping
from cleanEntries import cleanDate
from cleanEntries import stripComma

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def findElement(html, elementType, classCode):
    #given HTML code, return the FIRST element found with the particular class code

    for element in html.find_all(elementType):
        #print("element: ", element)
        if element.get("class") == None:
            continue
        else:
            className = (element.get("class"))[0]
            #print("className: ", className)

        #html handles classes weirdly
        #an element can have its classes separated by spaces
        if className.find(classCode) != -1 and element.contents != None:
            #print("found element: ", element)
            return element

    return "nothing found"

def findAllLetters(html, elementType, classCode):
    #a modified version of findElement

    #classCode is used to encrypt the letters that make up the sale date string
    #go through all the elements in the html subset with 'elementType'
    #   collect all the elements with the proper 'classCode' meanwhile filtering through the fake letters
    #   at the time of return, the string (ex. "Sold Jun 11, 2020") should be completed


    saleDate = ""
    for element in html.find_all(elementType):
        if element.get("class") == None:
            continue
        else:
            className = (element.get("class"))[0]

        #html handles classes weirdly
        #an element can have its classes separated by spaces
        if className.find(classCode) != -1 and element.contents != None:
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

def findClassName(html, elementType, content):
    #in the 'html' code, there is an element of 'elementType' which has 'content'
    #if the 'content' matches the element's .contents, then return the class name 'className'

    #USES
    #this 'className' is what ebay generated for every letter in the date
    #content is one letter in "Sold". we want to find the className that is common to all letters in "Sold"

    for element in html.find_all(elementType):
        if element.get("class") == None:
            continue
        else:
            className = (element.get("class"))[0]

        if len(element.contents) == 0:
            continue
        
        if element.contents[0] == content:
            #the class name is the KEY
            return className

    return "nothing found"

def findKey(html, elementType):
    #ebay changed the className of the element representing the sale date

    #this function will return the class name common to all of the sub elements in 'tagBlock' -- i regard the common className as the "key"

    for listing in html.find_all(elementType):
        tagBlock = findElement(listing, "div", "s-item__title--tagblock")

        if tagBlock == "nothing found":
            #bad listing
            continue
        else:
            tagBlock = tagBlock.contents
            
        letters = ["S", "o", "l", "d"]
        keys = []

        for letter in letters:
            #find a key
            keys.append( findClassName(tagBlock[0], "span", letter) )

        if len(set(keys)) == 1:
            #all the keys are identical
            return keys[0]

def findLink(html, elementType, classCode):

    element = findElement(html, elementType, classCode)

    if element == "nothing found":
        return "nothing found"
    else:
        return element.get("href")

def extract(rawGetFunction, html, elementType, className, cleanFunction):
    #this function will return algorithm-friendly data that is in the html block

    #use the analogy of the coconut
    #html is the entire coconut
    #the coconut fruit can be described with 'elementType' and 'className'
    #rawGetFunction peels away all the extra parts of the coconut and, after some work, we get the fruit
    #cleanFunction will alter the fruit so it is edible


    #html is a subset of the page's entire html we are examining

    #the rawGetFunction zooms in even more on this html and extracts a single HTML element of 'elementType' and 'className'
    #   in the case of finding the sale date, rawGetFunction straight up returns the fruit
    raw = rawGetFunction(html, elementType, className)
    
    if raw == "nothing found":
        #bad listing
        return False
    elif type(raw) == str:
        #raw is in a usable form as is
        fruit = raw
    else:
        fruit = raw.contents

    #nested HTML element?
    try:
        #this means that the item has been sold
        #items that have been sold on ebay have an extra span element NESTED
        fruit = fruit[0].contents

        """#changes#"""
        #fruit = fruit[0].contents[0]
    except:
        #the object is a string, and the element's contents are already accessible
        pass


    #by this point in the code, fruit is the content of the element

    #turn the fruit from ebay into a usable format for my algorithm
    data = cleanFunction(fruit)

    return data

def specialExtractNested(rawGetFunction, html, outerElementType, outerClassName, innerElementType, innerClassName, cleanFunction):
    outerBlock = findElement(html, outerElementType, outerClassName)

    if outerBlock == "nothing found":
        #bad listing
        return False
    else:
        outerBlock = outerBlock.contents

    raw = outerBlock[0].contents[0]

    return cleanFunction(raw)

def extractNested(rawGetFunction, html, outerElementType, outerClassName, innerElementType, innerClassName, cleanFunction):
    outerBlock = findElement(html, outerElementType, outerClassName)

    if outerBlock == "nothing found":
        #bad listing
        return False
    else:
        outerBlock = outerBlock.contents

    cleaned_inner = extract(rawGetFunction, outerBlock[0], innerElementType, innerClassName, cleanFunction)

    return cleaned_inner

def searchListings(html, elementType, classCode, itemCollection):
    #find all "elementType" HTML elements
    #extract data to make Item objects
    #search all posted listings and make an ProductList object


    #ebay tries to mess with the sale date and my code
    #right before the code starts, I will find the special className that can be used to find the sale date!
    key = findKey(html, elementType)

    for listing in html.find_all(elementType):
        if listing.get("class") == None:
            continue
        else:
            className = (listing.get("class"))[0]

        #the HTML element type is a listing part
        if className == classCode:
            #in this block, we extract data from a single listing
            
            #extract the title
            title = extract(findElement, listing, "h3", "s-item__title", cleanTitle)

            #extract the price
            price = extract(findElement, listing, "span", "s-item__price", cleanPrice)

            #extract shipping
            shipping = extract(findElement, listing, "span", "s-item__shipping", cleanShipping)

            #find sale date
            date = extractNested(findAllLetters, listing, "div", "s-item__title--tagblock", "span", key, cleanDate)

            if title == False or price == False or shipping == False or date == False:
                #bad listing
                continue
            else:
                #good listing

                #add shipping to price
                totalCost = round(price+shipping, 2)
                itemCollection.addItem( Item(title, totalCost, date) )

def aboutALink(link, exportFile, priceOutlier = None):

    productCollection = ProductList()

    totalTime = 0

    #get html and organize it
    raw_html = simple_get(link)
    html = BeautifulSoup(raw_html, 'html.parser')

    total_listings = specialExtractNested(findElement, html, "h1", "srp-controls__count-heading", "span", "BOLD", stripComma)
    max_iteration = int(int(total_listings)/200 +1)

    print("max: ", max_iteration)

    count = 0
    while count < 1:
        timeStart = time.time()

        searchListings(html, "li", "s-item", productCollection)


        link = findLink(html, "a", "pagination__next")
        count += 1

        #get html and organize it
        raw_html = simple_get(link)
        html = BeautifulSoup(raw_html, 'html.parser')
        timeEnd = time.time()

        #print(timeEnd - timeStart)
        print("count: ", count)
        totalTime += (timeEnd- timeStart)

    print("done")
    averageTime = round(totalTime/count, 2)
    print("average time: ", averageTime)

    #----------------------productCollection.removePriceOutliers(priceOutlier)
    productCollection.finishedCollectingListings()
    productCollection.exportData(exportFile)
    #analyze the data
    print(f"Average Price sold at auction: {productCollection.averagePriceSold}")


chromedriver = "C:\webdrivers\chromedriver"
#driver = webdriver.Chrome(chromedriver)

#process of downloading html and iterating over pages
#   request the link and download the html
#   while waiting a certain time so num requests per min is low
#       analyze the listings and add onto productCollection
#   when analyzing the page is done
#       if necessary, wait longer before next request
#   make next request, REPEAT


#ti-83, ti-84, ti-89
linkList = ["https://www.ebay.com/sch/i.html?_from=R40&_nkw=ti-83+calculators&_sacat=0&_ipg=200&LH_Sold=1&LH_Complete=1&rt=nc&LH_All=1", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=ti-84+calculators&_sacat=0&LH_TitleDesc=0&_fsrp=1&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=ti-89+calculator&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+galaxy+s4&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+galaxy+s5&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+galaxy+s6&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+galaxy+s7&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+galaxy+s8&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+galaxy+s9&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+galaxy+s10&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200",
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+6+plus&_sacat=9355&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+6&_sacat=9355&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&rt=nc&Model=Apple%2520iPhone%25206&_dcat=9355", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+7+plus&_sacat=9355&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR12.TRC2.A0.H0.Xiphone+7.TRS0&_nkw=iphone+7&_sacat=9355&LH_TitleDesc=0&_osacat=9355&_odkw=iphone+8+plus&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+8+plus&_sacat=9355&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR12.TRC2.A0.H0.Xiphone+8.TRS0&_nkw=iphone+8&_sacat=9355&LH_TitleDesc=0&_osacat=9355&_odkw=iphone+xs+max&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR11.TRC3.A0.H0.Xiphone+xs+max.TRS1&_nkw=iphone+xs+max&_sacat=9355&LH_TitleDesc=0&_osacat=9355&_odkw=iphone+xs&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+xs&_sacat=9355&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+xr&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR12.TRC2.A0.H0.Xiphone+x.TRS0&_nkw=iphone+x&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=iphone+11+pro&LH_Complete=1&rt=nc&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR11.TRC2.A0.H0.Xiphone+11+pro.TRS1&_nkw=iphone+11+pro&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=iphone+11+pro+max&LH_Complete=1&rt=nc&LH_Sold=1&_ipg=200", 
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+11+pro+max&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_ipg=200",
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+11&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_ipg=200",
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=galaxy+note+5&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200",
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=galaxy+note+8&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_ipg=200",
            "https://www.ebay.com/sch/i.html?_from=R40&_nkw=Samsung+galaxy+note+9&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_ipg=200"]

exportFileList = ["ti-83.csv", 
                    "ti-84.csv", 
                    "ti-89.csv", 
                    "s4.csv", 
                    "s5.csv", 
                    "s6.csv", 
                    "s7.csv", 
                    "s8.csv", 
                    "s9.csv", 
                    "s10.csv",
                    "iPhone6_plus.csv", 
                    "iPhone6.csv", 
                    "iPhone7_plus.csv", 
                    "iPhone7.csv", 
                    "iPhone8_plus.csv", 
                    "iPhone8.csv", 
                    "iPhone_XS_Max.csv", 
                    "iPhone_XS.csv", 
                    "iPhone_XR.csv", 
                    "iPhone_X.csv", 
                    "iPhone_11_Pro.csv", 
                    "iPhone_11_Pro_Max.csv",
                    "iPhone11.csv",
                    "GalaxyNote5.csv",
                    "GalaxyNote8.csv",
                    "GalaxyNote9.csv"]

#making new files
"""
for i in list(range(len(exportFileList)))[23:]:
    with open(exportFileList[i], "w") as file:
        pass
print("done")
sys.exit()
"""


#data collection sequence
for i in list(range(len(exportFileList)))[0:1]:
    print("doing: ", exportFileList[i])
    #aboutALink(driver, linkList[i], exportFileList[i], outlierList[i])
    #aboutALink(driver, linkList[i], exportFileList[i])
    aboutALink(linkList[i], exportFileList[i])
    print("done with: ", exportFileList[i])
    #time.sleep(10)

print("done")



sys.exit()

pdf = FPDF()


#data import sequence

listOfProductData = []
for i in list(range(len(exportFileList))):
    #print("doing: ", exportFileList[i])

    tempProduct = ProductList()
    tempProduct.importData(exportFileList[i])
    listOfProductData.append( tempProduct )


for i in list(range(len(exportFileList))):
    print("having fun with: ", exportFileList[i][:-4])
    listOfProductData[i].makeMonthlyCollection( exportFileList[i][:-4] )
   
    pdf.add_page()
    pdf.image(f"{exportFileList[i][:-4]}_avgPrice.png")
    pdf.add_page()
    pdf.image(f"{exportFileList[i][:-4]}_volume.png")

print("done")
pdf.output('visualization.pdf', 'F')
webbrowser.open_new(r'file://C:\Users\nimar\Desktop\Ebay\visualization.pdf')
