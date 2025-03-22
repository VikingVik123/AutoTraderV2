import time
from autotrader.dataframes.data import Price2DataFrame
from autotrader.indicators.technical import Technical_Indicators
from autotrader.strategies.default import DefaultStrategy
from autotrader.portfolio.account import SimAccount
from autotrader.exchanges.exchange import exch
from autotrader.db.database import SessionLocal
from autotrader.models.symbol import Symbol
from autotrader.data.get_history import Get_history
from autotrader.data.fetch import Fetch_price

class TradingEngine:
    def __init__(self):
        """Initialize the trading engine with data, indicators, strategy, and simulation account."""
        self.data = Price2DataFrame().to_dataframe()
        self.indicators = Technical_Indicators()
        self.strategy = DefaultStrategy()
        self.account = SimAccount()
        self.history = Get_history()
        self.fetch_price = Fetch_price()
    
    def run(self, interval=10):
        """Continuously checks for trading signals and executes trades."""
        while True:
            self.refresh_data()
            self.execute_trades()
            time.sleep(interval)
    
    def refresh_data(self):
        """Refresh market data, fetch new prices, and calculate indicators."""
        #self.history.save()  # Save historical data
        self.fetch_price.save()  # Fetch and save latest price
        self.data = Price2DataFrame().to_dataframe()
        self.data = self.indicators.get_indicators()
        self.strategy.data = self.data  # Update strategy with new data
    
    def execute_trades(self):
        """Executes trades based on strategy signals."""
        self.data = self.strategy.long_signal()
        self.data = self.strategy.short_signal()
        
        latest_signal = self.data.iloc[-1].get("signal", 0)
        
        if latest_signal == 1:
            order = self.account.long_order()
            print(f"Long Order Executed: {order}")
        elif latest_signal == -1:
            order = self.account.short_order()
            print(f"Short Order Executed: {order}")
        else:
            print("No trade signal detected.")
    
    def get_trading_summary(self):
        """Returns the current balance and open positions."""
        balance = self.account.get_balance()
        positions = self.account.trades
        return {"balance": balance, "open_positions": positions}

# Example usage:
if __name__ == "__main__":
    engine = TradingEngine()
    engine.run(interval=60)
