from datetime import datetime


class CryptoTransaction:
    def __init__(self, name, amount, price, date=None):
        self.name = name
        self.amount = amount
        self.price = price
        self.date = date or datetime.now()


class BuyTransaction(CryptoTransaction):
    def __init__(self, name, amount, price, date=None):
        super().__init__(name, amount, price, date)
        # self.transaction_type = 'buy'


class SellTransaction(CryptoTransaction):
    def __init__(self, name, amount, sell_price, purchase_price, date=None):
        super().__init__(name, amount, sell_price, date)
        self.purchase_price = purchase_price
        self.gain = (self.price - self.purchase_price) * self.amount
        # self.transaction_type = 'sell'
    #
    # @property
    # def gain(self):
    #     """Calculate and return the gain or loss from this sale."""
    #     total_cost = self.amount * self.purchase_price
    #     total_sale = self.amount * self.price
    #     return total_sale - total_cost

