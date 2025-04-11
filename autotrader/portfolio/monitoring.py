from autotrader.portfolio.account import SimAccount
from datetime import datetime
from autotrader.dataframes.data import Price2DataFrame

class MonitorTrades:
    def __init__(self, account: SimAccount):
        self.account = account

    def roi(self):
        if not self.account.trade_history:
            return {"error": "No trades available to calculate ROI"}

        total_investment = sum(t["quantity"] * t["entry_price"] for t in self.account.trade_history)
        current_value = sum(t["quantity"] * t["exit_price"] for t in self.account.trade_history)

        if total_investment == 0:
            return {"error": "No valid investment to calculate ROI"}

        roi_percentage = ((current_value - total_investment) / total_investment) * 100
        return {"ROI (%)": round(roi_percentage, 2)}

    def live_trade(self):
        if not self.account.open_position:
            return {"error": "No active trade"}
        df = Price2DataFrame().to_dataframe()
        self.account.update_dataframe(df)
        current_time = datetime.utcnow()
        trade_time = datetime.strptime(self.account.open_position["timestamp"], "%Y-%m-%d %H:%M:%S")
        trade_duration = current_time - trade_time
        latest_price = self.account.get_latest_price()
        entry_price = self.account.open_position["entry_price"]
        quantity = self.account.open_position["quantity"]
        side = self.account.open_position["side"]

        if side == "LONG":
            profit_loss = (latest_price - entry_price) * quantity
        else:
            profit_loss = (entry_price - latest_price) * quantity

        status = {
            "trade_duration": str(trade_duration),
            "symbol": self.account.open_position["symbol"],
            "side": side,
            "entry_price": entry_price,
            "quantity": quantity,
            "current_price": latest_price,
            "profit/loss": round(profit_loss, 2),
            "unrealized_pnl": self.account.unrealized_pnl(),
        }
        return status

    def positions(self):
        if not self.account.trade_history:
            return "No open positions (Simulated)."

        positions = "Open Positions (Simulated):\n"
        for order in self.account.trade_history:
            positions += f"Symbol: {order['symbol']}, Side: {order['side']}, Amount: {order['quantity']}, Price: {order['entry_price']}\n"
        return positions
