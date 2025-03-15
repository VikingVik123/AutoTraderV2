from autotrader.exchanges.exchange import exch
import json
import os
from autotrader.dataframes.data import dataframe

config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

symbol = config["symbol"]


class SimAccount:
    def __init__(self):
        self.exchange = exch.set_binance()
        self.balance = 100

    def get_balance(self):
        """
        gets simulated balance balance
        """
        return self.balance
    
    def get_latest_price(self):
        """Gets the latest close price from dataframe."""
        if dataframe.empty:
            raise ValueError("No price data available.")
        return dataframe["close"].iloc[-1]
    
    def order_amount(self, price):
        """Calculates the amount of asset to buy based on 10% of balance."""
        return (self.balance * 0.1) / price
    
    def buy_order(self):
        """Simulates a buy order."""
        # Simulate placing a buy order
        price = self.get_latest_price()
        amount = self.order_amount(price)
        if amount <= 0:
                return {"error": "Insufficient balance for order"}
        
        buy_order = self.exchange.create_limit_buy_order(symbol, amount, price)
        
        self.balance -= price * amount
        return buy_order
        
    
sim_account = SimAccount()
order_response = sim_account.buy_order()
print(order_response)
print("New balance:", sim_account.get_balance())
