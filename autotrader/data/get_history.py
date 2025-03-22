import os
import json
import requests
from autotrader.exchanges.exchange import exch
from datetime import datetime
from autotrader.db.database import SessionLocal
from autotrader.models.symbol import Symbol


# Get the path to config.json (correcting the location)
config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")

# Load config.json
with open(config_path, "r") as f:
    config = json.load(f)

# Extract values
timeframe = config["timeframe"]
symbol = config["symbol"]


class Get_history:
    def __init__(self):
        self.exchange = exch.set_binance()
        self.session = SessionLocal()
    def get_history(self):
        """
        Gets the last 200 candles from the exchange.
        """
        limit = 200
        try:
            hist_prices = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return hist_prices
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None
        
    def save(self):
        """
        Saves the historical data to the database.
        """
        hist_prices = self.get_history()
        
        if hist_prices:
            for price in hist_prices:
                dt_object = datetime.utcfromtimestamp(price[0] / 1000)
                ohlcv = Symbol(
                    datetime=dt_object,
                    open=price[1],
                    high=price[2],
                    low=price[3],
                    close=price[4],
                    volume=price[5]
                )
                self.session.add(ohlcv)
            self.session.flush()
            self.session.commit()
        self.session.close()

