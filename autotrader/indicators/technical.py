import pandas_ta as pta
from autotrader.dataframes.data import dataframe
import pandas as pd


class Technical_Indicators:
    def __init__(self):
        self.data = dataframe

    def get_indicators(self):
        """
        Returns a dataframe with the technical indicators
        """
        if self.data.empty or self.data is None:
            return pd.DataFrame()
        
        self.data["rsi"] = pta.rsi(self.data["close"], length=14)
        self.data["ema200"] = pta.ema(self.data["close"], length=200)
        self.data["ema50"] = pta.ema(self.data["close"], length=50)
        self.data["sma200"] = pta.sma(self.data["close"], length=200)
        self.data["sma50"] = pta.sma(self.data["close"], length=50)
        
        return self.data
    
    def hvi(self, dataframe, period=10):
        """
        recreate the highest volume indicator from tradingview
        """
        HV = dataframe['volume'].rolling(window=period).max()
        HVI = (dataframe["volume"] / HV) * 100
        return HVI
    
    def supertrend(self):
        """
        defines the supertrend indicator from pandas_ta
        """
        periodo = 10
        atr_multiplicador = 3.0

        st = pta.supertrend(self.data["high"],
                            self.data["low"],
                            self.data["close"],
                            length=periodo,
                            multiplier=atr_multiplicador
                        )

        self.data["supertrend"] = st.iloc[:, 0]  # Supertrend line
        self.data["supertrend_signal"] = st.iloc[:, 1]  # -1 = Downtrend, 1 = Uptrend
        return self.data