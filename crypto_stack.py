# module imports
from transactions import BuyTransaction, SellTransaction

# third-party imports
from collections import deque
import pandas as pd


class CryptoStack:
    def __init__(self, name):
        self.name = name
        self.stack = deque()

    def buy(self, amount, price):
        self.stack.append(BuyTransaction(self.name, amount, price))

    def sell(self, amount_to_sell, sell_price):
        if self.is_empty():
            print("No tokens to sell!")
            return None

        total_gain = 0
        amount_remaining = amount_to_sell

        while amount_remaining > 0 and not self.is_empty():
            recent_purchase = self.stack.pop()
            if recent_purchase.amount > amount_remaining:
                # Partial sale from the recent purchase
                gain = SellTransaction(self.name, amount_remaining, sell_price).calculate_gain(recent_purchase.price)
                total_gain += gain
                print(f"Sold {amount_remaining} of {self.name} for {sell_price} each. Partial gain: {gain}")

                # Update the recent purchase with the remaining amount and put it back
                recent_purchase.amount -= amount_remaining
                self.stack.append(recent_purchase)
                amount_remaining = 0  # Fully sold the requested amount
            else:
                # Full sale of the recent purchase, might need to continue selling from earlier purchases
                gain = SellTransaction(self.name, recent_purchase.amount, sell_price).calculate_gain(recent_purchase.price)
                total_gain += gain
                print(f"Sold {recent_purchase.amount} of {self.name} for {sell_price} each. Partial gain: {gain}")

                amount_remaining -= recent_purchase.amount  # Update the remaining amount to sell

        if amount_remaining > 0:
            print(f"Not enough tokens were available to sell. {amount_remaining} of {self.name} remaining to sell.")

        return total_gain

    def is_empty(self):
        return len(self.stack) == 0

    def show_stack(self):
        return [vars(token) for token in self.stack]


if __name__=='__main__':
    # Creating separate stack objects for Bitcoin
    bitcoin_stack = CryptoStack('Bitcoin')

    # Example transactions
    bitcoin_stack.buy(1, 50000)
    bitcoin_stack.buy(0.5, 52000)
    bitcoin_stack.sell(1.2, 51000)

    print("Bitcoin Stack:", bitcoin_stack.show_stack())

