from autotrader.portfolio.account import SimAccount
from datetime import datetime

class MonitorTrades(SimAccount):
    def __init__(self):
        super().__init__()

    def roi(self):
        """Calculate ROI (Return on Investment) for open trades."""
        if not self.trades:
            return {"error": "No trades available to calculate ROI"}

        total_investment = sum(trade["quantity"] * trade["price"] for trade in self.trades)
        current_value = sum(trade["quantity"] * self.get_latest_price() for trade in self.trades)

        if total_investment == 0:
            return {"error": "No valid investment to calculate ROI"}

        roi_percentage = ((current_value - total_investment) / total_investment) * 100
        return {"ROI (%)": round(roi_percentage, 2)}
    
    def live_trade(self):
        """Show the performance of an open trade."""
        if not self.trades:
            return {"error": "No active trades"}
        
        current_time = datetime.utcnow()
        latest_trade = self.trades[-1]
        trade_time = datetime.strptime(latest_trade["timestamp"], "%Y-%m-%d %H:%M:%S")
        trade_duration = current_time - trade_time
        latest_price = self.get_latest_price()
        profit_loss = (latest_price - latest_trade["price"]) * latest_trade["quantity"]

        status = {
            "trade_duration": str(trade_duration),
            "symbol": latest_trade["symbol"],
            "side": latest_trade["side"],
            "price": latest_trade["price"],
            "quantity": latest_trade["quantity"],
            "current_price": latest_price,
            "profit/loss": round(profit_loss, 2),
            "roi": self.roi(),
        }
        return status
    
    def positions(self):
        positions = "Open Positions (Simulated):\n"
        for order in self.trades:
            positions += f"Symbol: {order['symbol']}, Side: {order[']side']}, Amount: {order['quantity']}, Price: {order['price']}\n"
        return positions if self.trades else "No open positions (Simulated)."

"""
if __name__ == "__main__":
    monitor = MonitorTrades()
    #monitor.long_order()
    print(monitor.positions())
"""
