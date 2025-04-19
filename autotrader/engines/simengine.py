import time
from autotrader.dataframes.data import Price2DataFrame
from autotrader.indicators.technical import Technical_Indicators
from autotrader.strategies.default import DefaultStrategy
from autotrader.portfolio.account import SimAccount
from autotrader.portfolio.monitoring import MonitorTrades
from autotrader.exchanges.exchange import exch
from autotrader.db.database import SessionLocal
from autotrader.models.symbol import Symbol
from autotrader.data.get_history import Get_history
from autotrader.data.fetch import Fetch_price

class TradingEngine:
    def __init__(self, account=None, monitor=None):
        """Initialize the trading engine with data, indicators, strategy, and simulation account."""
        self.data = Price2DataFrame().to_dataframe()
        self.indicators = Technical_Indicators()
        self.strategy = DefaultStrategy()
        self.account = account or SimAccount()
        self.monitor = monitor or MonitorTrades(self.account)
        self.history = Get_history()
        self.fetch_price = Fetch_price()

    def run(self, interval=60):
        """Continuously checks for trading signals and executes trades."""
        while True:
            self.refresh_data()
            self.execute_trades()
            self.monitor_trades()
            time.sleep(interval)

    def refresh_data(self):
        """Refresh market data, fetch new prices, and calculate indicators."""
        self.fetch_price.save()
        df = Price2DataFrame().to_dataframe()
        df_indicators = self.indicators.get_indicators()
        self.account.update_dataframe(df_indicators)
        self.strategy.data = df_indicators  # Ensure strategy uses updated data

    def execute_trades(self):
        """Executes trades based on strategy signals."""
        latest_signal = self.strategy.long_signal().iloc[-1].get("signal", 0)
        if latest_signal == 1:
            order = self.account.long_order()
            print(f"Long Order Executed: {order}")

        latest_signal = self.strategy.short_signal().iloc[-1].get("signal", 0)
        if latest_signal == -1:
            order = self.account.short_order()
            print(f"Short Order Executed: {order}")

        if latest_signal == 0:
            print("No trade signal detected.")

    def monitor_trades(self):
        """Monitor the performance of open trades."""
        roi = self.monitor.roi()
        live_trade = self.monitor.live_trade()

        if live_trade.get("error"):
            print(f"Error: {live_trade['error']}")
            return

        entry = live_trade["entry_price"]
        roi = (live_trade["current_price"] - entry) / entry
        if live_trade["side"] == "SHORT":
            roi *= -1

        if roi >= 0.03 or roi <= -0.02:  # Take profit or stop loss
            close_trade = self.account.close_trade()
            print(f"Position closed with PnL: {close_trade['pnl']}")
        else:
            print(f"Live Trade: {live_trade}")

    def get_trading_summary(self):
        """Returns the current balance and open positions."""
        balance = self.account.get_balance()
        positions = self.monitor.live_trade()
        return {"balance": balance, "open_positions": positions}
