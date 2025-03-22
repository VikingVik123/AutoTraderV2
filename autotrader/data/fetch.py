from autotrader.models.symbol import Symbol
from autotrader.exchanges.exchange import exch
from autotrader.db.database import SessionLocal
import json
import os
from datetime import datetime

# Get the path to config.json (correcting the location)
config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")

# Load config.json
with open(config_path, "r") as f:
    config = json.load(f)

# Extract values
timeframe = config["timeframe"]
symbol = config["symbol"]

class Fetch_price:
    def __init__(self):
        self.exchange = exch.set_binance()
        self.session = SessionLocal()

    def fetch_price(self):
        """
        gets price from exchange
        """
        prices = self.exchange.fetch_ohlcv(symbol, timeframe, limit=1)
        return prices
    
    def save(self):
        """
        saves price to database
        """
        prices = self.fetch_price()
        if prices:
            price = prices[0]
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