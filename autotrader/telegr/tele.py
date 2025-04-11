from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os
import json
from autotrader.portfolio.account import SimAccount
from autotrader.portfolio.monitoring import MonitorTrades

config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

token = config["telegram"]["token"]
chat_id = config["telegram"]["chatId"]

class TeleComm:
    """
    Handles Telegram communication for a single-symbol paper trading bot.
    """
    def __init__(self, token: str, chat_id: str, account: SimAccount, monitor: MonitorTrades):
        self.token = token
        self.chat_id = chat_id
        self.port = account
        self.monitor = monitor
        self.application = Application.builder().token(token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("balance", self.balance))
        self.application.add_handler(CommandHandler("long", self.long))
        self.application.add_handler(CommandHandler("short", self.short))
        self.application.add_handler(CommandHandler("close", self.close))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("trades", self.trades))

        self.reply_keyboard = [
            ['/start', '/stop'],
            ['/balance', '/status'],
            ['/long', '/short'],
            ['/trades', '/close']
        ]
        self.reply_markup = ReplyKeyboardMarkup(self.reply_keyboard, resize_keyboard=True)

    async def start(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("👋 Welcome to AutoTrader!", reply_markup=self.reply_markup)

    async def stop(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("🛑 Stopping AutoTrader.")
        self.application.stop()

    async def balance(self, update: Update, context: CallbackContext) -> None:
        balance = self.port.get_balance()
        await update.message.reply_text(f"💰 Current balance: ${balance}", reply_markup=self.reply_markup)

    async def long(self, update: Update, context: CallbackContext) -> None:
        order = self.port.long_order()
        if "error" in order:
            await update.message.reply_text(f"⚠️ {order['error']}", reply_markup=self.reply_markup)
        else:
            await update.message.reply_text(
                f"✅ Long position opened\nPrice: {order['entry_price']:.2f}\nQty: {order['quantity']:.6f}",
                reply_markup=self.reply_markup,
            )

    async def short(self, update: Update, context: CallbackContext) -> None:
        order = self.port.short_order()
        if "error" in order:
            await update.message.reply_text(f"⚠️ {order['error']}", reply_markup=self.reply_markup)
        else:
            await update.message.reply_text(
                f"✅ Short position opened\nPrice: {order['entry_price']:.2f}\nQty: {order['quantity']:.6f}",
                reply_markup=self.reply_markup,
            )

    async def close(self, update: Update, context: CallbackContext) -> None:
        close_trade = self.port.close_trade()
        if "error" in close_trade:
            await update.message.reply_text(f"⚠️ {close_trade['error']}", reply_markup=self.reply_markup)
        else:
            await update.message.reply_text(
                f"💼 Position Closed:\n"
                f"Side: {close_trade['side']}\n"
                f"Entry: {close_trade['entry_price']:.2f}\n"
                f"Exit: {close_trade['exit_price']:.2f}\n"
                f"Qty: {close_trade['quantity']:.6f}\n"
                f"PnL: ${close_trade['pnl']:.2f}",
                reply_markup=self.reply_markup,
            )

    async def status(self, update: Update, context: CallbackContext) -> None:
        status = self.monitor.live_trade()
        if isinstance(status, dict) and "error" in status:
            await update.message.reply_text(status["error"], reply_markup=self.reply_markup)
        else:
            await update.message.reply_text(f"Live trade: {status}", reply_markup=self.reply_markup)
            

    async def trades(self, update: Update, context: CallbackContext) -> None:
        if not self.port.trade_history:
            await update.message.reply_text("🗃 No trade history yet.", reply_markup=self.reply_markup)
            return

        msg = "📈 Trade History:\n"
        for i, t in enumerate(self.port.trade_history[-5:], 1):
            msg += (
                f"\nTrade {i} - {t['side']}:\n"
                f"  Entry: {t['entry_price']:.2f}, Exit: {t['exit_price']:.2f}\n"
                f"  Qty: {t['quantity']:.6f}, PnL: ${t['pnl']:.2f}\n"
                f"  Closed at: {t['closed_at']}\n"
            )
        await update.message.reply_text(msg, reply_markup=self.reply_markup)

    def run(self):
        """Starts the bot."""
        self.application.run_polling()

"""
if __name__ == "__main__":
    account = SimAccount()
    monitor = MonitorTrades(account)
    tele_comm = TeleComm(token, chat_id, account, monitor)
    tele_comm.run()
"""