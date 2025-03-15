import ccxt
import os
from dotenv import load_dotenv

class Exchange:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.secret = os.getenv("API_SECRET")
    
    def set_binance(self):
        """
        sets binance as exchange
        """
        binance = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.secret,
        })
        return binance
    
    def set_kucoin(self):
        """
        sets kucoin as exchange
        """
        kucoin = ccxt.kucoin({
            'apiKey': self.api_key
        })
        return kucoin
    
    def set_bybit(self):
        """
        sets bybit as exchange
        """
        bybit = ccxt.bybit({
            'apiKey': self.api_key
        })
        return bybit
    
exch = Exchange()