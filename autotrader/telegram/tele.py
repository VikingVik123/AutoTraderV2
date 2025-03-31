from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.ext import CallbackContext
import os
import json
from autotrader.portfolio.account import SimAccount
from autotrader.portfolio.monitoring import MonitorTrades
from autotrader.engines.simengine import TradingEngine

config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

token = config["telegram"]["token"]
chat_id = config["telegram"]["chatId"]

class TeleComm:
    """
    Handles Telegram communication.
    """
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.port = SimAccount()
        self.application = Application.builder().token(token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("balance", self.balance))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("long", self.long))
        self.application.add_handler(CommandHandler("short", self.short))
        self.application.add_handler(CommandHandler("close", self.port.close_trade))

        self.reply_keyboard = [['/start', '/stop'], ['/balance', '/status'], ['/long', '/short'], ['/trades', '/close']]
        self.reply_markup = ReplyKeyboardMarkup(self.reply_keyboard, resize_keyboard=True)

    async def start(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("Welcome To AutoTrader")

    async def stop(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("Stopping AutoTrader")
        self.application.stop()

    async def balance(self, update: Update, context: CallbackContext) -> None:
        """Sends the current balance to the user."""
        balance = self.port.get_balance()
        await update.message.reply_text(f"Current balance: {balance}", reply_markup=self.reply_markup)

    async def long(self, update: Update, context: CallbackContext) -> None:
        """Simulates a long order."""
        order = self.port.long_order()
        if "error" in order:
            await update.message.reply_text(order["error"], reply_markup=self.reply_markup)
        else:
            await update.message.reply_text(f"Long order placed: {order}", reply_markup=self.reply_markup)

    async def short(self, update: Update, context: CallbackContext) -> None:
        """Simulates a short order."""
        order = self.port.short_order()
        if "error" in order:
            await update.message.reply_text(order["error"], reply_markup=self.reply_markup)
        else:
            await update.message.reply_text(f"Short order placed: {order}", reply_markup=self.reply_markup)

    async def trades(self, update: Update, context: CallbackContext) -> None:
        """Sends the current open trades to the user."""
        trades = MonitorTrades().positions()
        await update.message.reply_text(f"{trades}", reply_markup=self.reply_markup)
        if "error" in trades:
            await update.message.reply_text(trades["error"], reply_markup=self.reply_markup)
        else:
            await update.message.reply_text(f"Open trades: {trades}", reply_markup=self.reply_markup)

    async def close(self, update: Update, context: CallbackContext) -> None:
        """Closes the current open trade."""
        close_trade = self.port.close_trade()
        if "error" in close_trade:
            await update.message.reply_text(close_trade["error"], reply_markup=self.reply_markup)
        else:
            await update.message.reply_text(f"Trade closed: {close_trade}", reply_markup=self.reply_markup)

    async def status(self, update: Update, context: CallbackContext) -> None:
        """Sends the status of the current open trade."""
        status = MonitorTrades().live_trade()
        await update.message.reply_text(f"{status}", reply_markup=self.reply_markup)

    def run(self):
        """Starts the bot."""
        self.application.run_polling()
