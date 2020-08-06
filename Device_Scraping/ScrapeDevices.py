import sys
from fpdf import FPDF
import webbrowser

from Item import Item
from Product import ProductList

from links_csv_txt import linkList
from links_csv_txt import exportFileList

from ebayFunctions_Grand import aboutALink


chromedriver = "C:\webdrivers\chromedriver"
#driver = webdriver.Chrome(chromedriver)

#process of downloading html and iterating over pages
#   request the link and download the html
#   scrape data from the html
#   export the data

#process of importing and displaying the data
#   import the data into a series of ProductList() objects
#   per ProductList() object, graph its contents
#   print all the graphs into a single pdf sheet


#making new files
"""
for i in list(range(len(exportFileList)))[23:]:
    with open(exportFileList[i], "w") as file:
        pass
print("done")
sys.exit()
"""
#sys.exit()

#data collection sequence
for i in list(range(len(exportFileList))):
    print("doing: ", exportFileList[i])
    aboutALink(linkList[i], exportFileList[i])
    print("done with: ", exportFileList[i])
    #time.sleep(10)



pdf = FPDF()

#data visualization/import sequence

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

