import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("CSV_Collection/ti-83_plus_calculator_Auction.csv")
#read from the csv file
#make a data frame with columns -> ["title", "price", "date"]
#						rows -> individual listings

#print(df["price"].describe())
#print(df.dtypes)

by_date = df.groupby(["date"]).mean().reset_index() # group by date. find the mean of all entries for every date.
#note what reset_index() does. it returns a new DataFrame for which the previous index is now a column in the DataFrame!


fig, ax = plt.subplots()

plot = by_date.plot.scatter(
x = "date",
y = "price"
) 

plt.show()
