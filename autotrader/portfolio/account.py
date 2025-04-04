import json
import os
import time
import numpy as np
from autotrader.exchanges.exchange import exch
from autotrader.dataframes.data import Price2DataFrame

config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

symbol = config["symbol"]

class SimAccount:
    def __init__(self):
        self.exchange = exch.set_binance()
        self.balance = 100.0
        self.trades = []
        self.dataframe = Price2DataFrame().to_dataframe()

    def get_balance(self):
        """Gets simulated balance."""
        return self.balance
    
    def get_latest_price(self):
        """Gets the latest close price from dataframe."""
        if self.dataframe.empty:
            raise ValueError("No price data available.")
        return self.dataframe["close"].iloc[-1]
    
    def order_amount(self, price):
        """Calculates the amount of asset to buy based on 10% of balance."""
        return (self.balance * 0.1) / price
    
    def long_order(self):
        """Simulates a buy order."""
        price = float(self.get_latest_price())
        amount = float(self.order_amount(price))
        if amount <= 0:
            return {"error": "Insufficient balance for order"}
        
        order = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "symbol": symbol,
            "side": "LONG",
            "type": "MARKET",
            "quantity": amount,
            "price": price,
        }
        
        self.balance -= price * amount
        self.trades.append(order)
        return order
    
    def short_order(self):
        """Simulates a sell order."""
        price = float(self.get_latest_price())
        amount = float(self.order_amount(price))
        if amount <= 0:
            return {"error": "Insufficient balance for order"}
        
        order = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "symbol": symbol,
            "side": "SHORT",
            "type": "MARKET",
            "quantity": amount,
            "price": price,
        }
        
        self.balance += price * amount
        self.trades.append(order)
        return order
    
    def close_trade(self):
        """
        close any open trade
        """
        if not self.trades:
            return {"error": "No open trades to close"}
        
        trade = self.trades.pop()
        price = float(self.get_latest_price())
        profit = (price - trade["price"]) * trade["quantity"]
        
        if trade["side"] == "LONG":
            self.balance += price * trade["quantity"] + profit
        else:
            self.balance -= price * trade["quantity"] + profit
        
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "symbol": symbol,
            "side": trade["side"],
            "type": "MARKET",
            "quantity": trade["quantity"],
            "price": price,
            "profit": profit,
        }

    def save_trades(self, filename="trade_log.json"):
        """Logs trades to a JSON file."""
        with open(filename, "w") as f:
            json.dump(self.trades, f, indent=4)
 

