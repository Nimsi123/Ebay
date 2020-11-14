from bs4 import BeautifulSoup


from Ebay.Site_Operations.ebayFunctions_Grand import *

from Ebay.Site_Operations.traverseHtml import *
#findElement, findAllLetters, findKey, findLink

link = "https://www.ebay.com/b/Digital-Cameras/31388/bn_779"

raw_html = simple_get(link, True)
html = BeautifulSoup(raw_html, "html.parser")


elementType = "a"
attributeKey = "class"
attributeValue = "b-guidancecard__link"


linkList = []
for element in html.find_all(elementType):
    #print("element: ", element)
    if element.get(attributeKey) == None:
        continue
    else:
        className = (element.get(attributeKey))[0]
        #print("className: ", className)

    #html handles classes weirdly
    #an element can have its classes separated by spaces
    #print("attribute: ", attributeKey, attributeValue)
    #print("class name: ", className, "--", attributeValue)
    #print("truths: ", className.find(attributeValue), element.contents != None)
    if className.find(attributeValue) != -1 and element.contents != None:
    	try:
    		linkList.append(element.get("href"))
    		#print(element.contents[0].contents[0].get("alt"))
    	except:
    		pass

#<p class="b-guidancecard__title">Canon EOS 5D Mark II</p>
print(len(linkList))

deviceList = []
for link in linkList:
	raw_html = simple_get(link, True)
	html = BeautifulSoup(raw_html, "html.parser")

	elementType = "p"
	attributeKey = "class"
	attributeValue = "b-guidancecard__title"
	for element in html.find_all(elementType):
	    #print("element: ", element)
	    if element.get(attributeKey) == None:
	        continue
	    else:
	        className = (element.get(attributeKey))[0]
	        #print("className: ", className)

	    #html handles classes weirdly
	    #an element can have its classes separated by spaces
	    #print("attribute: ", attributeKey, attributeValue)
	    #print("class name: ", className, "--", attributeValue)
	    #print("truths: ", className.find(attributeValue), element.contents != None)
	    if className.find(attributeValue) != -1 and element.contents != None:
	    	try:
	    		deviceList.append(element.contents[0])
	    		#print(element.contents[0].contents[0].get("alt"))
	    	except:
	    		pass

print(len(deviceList))

message = "["
for device in deviceList:
	message += f"\"{device}\", "

message = message[:-2] + "]"
print(message)