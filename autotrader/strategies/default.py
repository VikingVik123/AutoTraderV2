from autotrader.dataframes.data import dataframe
from autotrader.indicators.technical import Technical_Indicators

class DefaultStrategy:
    """
    default trading strategy
    """
    def __init__(self):
        self.data = dataframe
        self.indicators = Technical_Indicators()

    def long_signal(self):
        """
        defines the long signal
        """
        self.data.loc[
            (self.data["close"] > self.data["ema50"]) &
            (self.data["close"] > self.data["sma200"]) &
            (self.data["ema50"] > self.data["sma200"])
        , "signal"] = 1
        return self.data
    
    def short_signal(self):
        """
        defines the short signal
        """
        self.data.loc[
            (self.data["close"] < self.data["ema50"]) &
            (self.data["close"] < self.data["sma200"]) &
            (self.data["ema50"] < self.data["sma200"])
        , "signal"] = -1
        return self.data

