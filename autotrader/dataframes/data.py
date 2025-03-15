from autotrader.models.symbol import Symbol
import pandas as pd
from autotrader.db.database import db
session = db.get_session()


class Price2DataFrame:
    def __init__(self):
        self.prices = session.query(Symbol).all()

    def to_dataframe(self):
        """
        Converts the prices to a pandas dataframe
        """
        if not self.prices:
            pd.DataFrame()

        data = {
            "datetime": [price.datetime for price in self.prices],
            "open": [price.open for price in self.prices],
            "high": [price.high for price in self.prices],
            "low": [price.low for price in self.prices],
            "close": [price.close for price in self.prices],
            "volume": [price.volume for price in self.prices]
        }
        dataframe = pd.DataFrame(data)
        session.close()
        return dataframe
    
dataframe = Price2DataFrame().to_dataframe()
# Function to get DataFrame
#def get_price_dataframe():
#    return Price2DataFrame().to_dataframe()