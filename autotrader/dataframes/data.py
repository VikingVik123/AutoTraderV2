import pandas as pd
from autotrader.db.database import SessionLocal
from autotrader.models.symbol import Symbol  # ✅ Import Symbol model
from autotrader.data.fetch import Fetch_price  # ✅ Import Fetch_price class
import time

class Price2DataFrame:
    def __init__(self):
        """Initialize and fetch all price data from the database."""
        session = SessionLocal()
        self.prices = session.query(Symbol).all()  # ✅ Specify table
        session.close()  # ✅ Close session after fetching data
        

    def to_dataframe(self):
        """
        Converts the prices to a pandas dataframe.
        """
        if not self.prices:
            return pd.DataFrame()

        data = {
            "datetime": [price.datetime for price in self.prices],
            "open": [price.open for price in self.prices],
            "high": [price.high for price in self.prices],
            "low": [price.low for price in self.prices],
            "close": [price.close for price in self.prices],
            "volume": [price.volume for price in self.prices],
        }
        return pd.DataFrame(data)

    #def test(self):
        """
        #Test the Price2DataFrame class.
        """
    #    while True:
    #        fetch = Fetch_price()
    #        fetch.save()
    #        price_df = Price2DataFrame().to_dataframe()
    #        print(price_df)
    #        time.sleep(60)
            
"""
if __name__ == "__main__":
    price = Price2DataFrame()
    print(price.to_dataframe())
"""