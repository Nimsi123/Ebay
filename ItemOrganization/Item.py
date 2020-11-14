class Item:
    def __init__(self, t, p, d):
        self.title = t
        self.price = p
        self.date = d

    def getTitle(self):
        return self.title

    def getPrice(self):
        return self.price

    def getDate(self):
        return self.date

    def get_dict_data(self):
        return {"title": self.title, "price": self.price, "date": self.date}

    def __eq__(self, other):
        return self.title == other.title and self.price == other.price and self.date == other.date

    def __str__(self):
        return f"{self.getTitle()} {self.getPrice()} {self.getDate()}"