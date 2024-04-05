# module imports
from transactions import BuyTransaction, SellTransaction

# third-party imports
from collections import deque
import pandas as pd


class CryptoDB:
    def __init__(self, name):
        self.name = name
        self.wallet = deque()
        self.capital_gains = deque()

    def buy(self, amount, price):
        self.wallet.append(BuyTransaction(self.name, amount, price))

    def sell(self, amount_to_sell, sell_price):
        if self.is_empty():
            print("No tokens to sell!")
            return None

        amount_remaining = amount_to_sell

        while amount_remaining > 0 and not self.is_empty():
            recent_purchase = self.wallet.pop()
            if recent_purchase.amount > amount_remaining:
                # Partial sale from the recent purchase
                transaction = SellTransaction(self.name, amount_remaining, sell_price, recent_purchase.price)
                self.capital_gains.append(transaction)
                print(f"Sold {amount_remaining} of {self.name} for {sell_price} each. Partial transaction: {transaction}")

                # Update the recent purchase with the remaining amount and put it back
                recent_purchase.amount -= amount_remaining
                self.wallet.append(recent_purchase)
                amount_remaining = 0  # Fully sold the requested amount
            else:
                # Full sale of the recent purchase, might need to continue selling from earlier purchases
                transaction = SellTransaction(self.name, recent_purchase.amount, sell_price, recent_purchase.price)
                self.capital_gains.append(transaction)
                print(f"Sold {recent_purchase.amount} of {self.name} for {sell_price} each. Partial transaction: {transaction}")

                amount_remaining -= recent_purchase.amount  # Update the remaining amount to sell

        if amount_remaining > 0:
            print(f"Not enough tokens were available to sell. {amount_remaining} of {self.name} remaining to sell.")

    def total_gains(self):
        return sum([capital_gain.gain for capital_gain in self.capital_gains])

    def is_empty(self):
        return len(self.wallet) == 0

    def wallet_to_dict(self):
        return [vars(token) for token in self.wallet]

    def capital_gains_to_dict(self):
        return [vars(gain) for gain in self.capital_gains]

    def wallet_df(self):
        return pd.DataFrame([vars(token) for token in self.wallet])

    def capital_gains_df(self):
        return pd.DataFrame([vars(gain) for gain in self.capital_gains])


if __name__=='__main__':
    # Creating separate stack objects for Bitcoin
    bitcoin_stack = CryptoDB('Bitcoin')

    # Example transactions
    bitcoin_stack.buy(1, 50000)
    bitcoin_stack.buy(0.5, 52000)
    bitcoin_stack.sell(1.2, 51000)
    bitcoin_stack.buy(0.8, 33000)
    bitcoin_stack.sell(0.5, 54000)
    bitcoin_stack.buy(0.5, 45000)
    bitcoin_stack.sell(0.1, 48000)

    print("Current Bitcoin Wallet:\n", bitcoin_stack.wallet_df())
    print("DB of Bitcoin Gains:\n", bitcoin_stack.capital_gains_df())

