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
        self.transaction_type = 'buy'


class SellTransaction(CryptoTransaction):
    def __init__(self, name, amount, sell_price, date=None):
        super().__init__(name, amount, sell_price, date)
        self.transaction_type = 'sell'

    def calculate_gain(self, purchase_price):
        """Calculate and return the gain or loss from this sale."""
        total_cost = self.amount * purchase_price
        total_sale = self.amount * self.price
        return total_sale - total_cost