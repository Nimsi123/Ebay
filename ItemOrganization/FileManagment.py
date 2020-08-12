import os


#making new files
def fileCheck(item, makeLink, csvSubDirectory, pngSubDirectory):

    item = item.replace(" ", "_")

    path = os.path.join(csvSubDirectory, f"{item}.csv")
    #print(path)
    try:
        with open(path, "r") as file:
            pass
    except:
        with open(path, "w") as file:
            pass

    path = os.path.join(pngSubDirectory, item + "_avgPrice.png")
    #print(path)
    try:
        with open(path, "r") as file:
            pass
    except:
        with open(path, "w") as file:
            pass

    path = os.path.join(pngSubDirectory, item + "_volume.png")
    #print(path)
    try:
        with open(path, "r") as file:
            pass
    except:
        with open(path, "w") as file:
            pass

    if makeLink:
        #make its link
        link = getEbayLink("All Listings", item)

        path = os.path.join(csvSubDirectory, "link.csv")
        with open(path, "a", encoding = "utf-8") as file:
            data = ["link"]
            csv_writer = csv.DictWriter(file, fieldnames = data)
            csv_writer.writerow({"link": link})
