import json
import os
import time
from autotrader.exchanges.exchange import exch
from autotrader.dataframes.data import Price2DataFrame

config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

symbol = config["symbol"]

class SimAccount:
    def __init__(self, dataframe=None):
        self.exchange = exch.set_binance()
        self.balance = 100.0
        self.open_position = None
        self.trade_history = []
        self.dataframe = dataframe or Price2DataFrame().to_dataframe()

    def update_dataframe(self, df):
        self.dataframe = df

    def get_balance(self):
        return round(self.balance, 2)

    def get_latest_price(self):
        df = self.dataframe
        if df.empty:
            raise ValueError("No price data available.")
        return float(df["close"].iloc[-1])

    def order_amount(self, price):
        return (self.balance * 0.1) / price

    def long_order(self):
        if self.open_position:
            return {"error": "Position already open. Close it first."}

        price = self.get_latest_price()
        qty = self.order_amount(price)

        if qty <= 0:
            return {"error": "Insufficient balance for long order"}

        self.open_position = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "symbol": symbol,
            "side": "LONG",
            "quantity": qty,
            "entry_price": price,
        }

        self.balance -= price * qty
        return {"status": "Long position opened", **self.open_position}

    def short_order(self):
        if self.open_position:
            return {"error": "Position already open. Close it first."}

        price = self.get_latest_price()
        qty = self.order_amount(price)

        if qty <= 0:
            return {"error": "Insufficient balance for short order"}

        self.open_position = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "symbol": symbol,
            "side": "SHORT",
            "quantity": qty,
            "entry_price": price,
        }

        self.balance += price * qty
        return {"status": "Short position opened", **self.open_position}

    def close_trade(self):
        if not self.open_position:
            return {"error": "No open position to close"}

        price = self.get_latest_price()
        pos = self.open_position
        qty = pos["quantity"]
        entry = pos["entry_price"]

        if pos["side"] == "LONG":
            pnl = (price - entry) * qty
            self.balance += price * qty
        else:
            pnl = (entry - price) * qty
            self.balance -= price * qty

        trade_record = {
            "symbol": pos["symbol"],
            "side": pos["side"],
            "entry_price": entry,
            "exit_price": price,
            "quantity": qty,
            "pnl": round(pnl, 2),
            "closed_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
        }

        self.trade_history.append(trade_record)
        self.open_position = None

        return {"status": "Position closed", **trade_record}

    def unrealized_pnl(self):
        if not self.open_position:
            return {"error": "No open position"}

        price = self.get_latest_price()
        entry = self.open_position["entry_price"]
        qty = self.open_position["quantity"]
        side = self.open_position["side"]

        if side == "LONG":
            pnl = (price - entry) * qty
        else:
            pnl = (entry - price) * qty

        return {"unrealized_pnl": round(pnl, 2)}

    def save_trade_history(self, filename="trade_history.json"):
        with open(filename, "w") as f:
            json.dump(self.trade_history, f, indent=4)
