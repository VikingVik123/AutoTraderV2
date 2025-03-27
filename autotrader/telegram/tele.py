from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
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
    handles telegram communication
    """
    def __init__(self):
        self.token = token
        self.chat_id = chat_id
        self.bot = Bot(token=self.token)
        self.sim_account = SimAccount()
        self.monitor = MonitorTrades()
        self.updater = Updater(self.token)
        self.dp = self.updater.dispatcher
        
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("balance", self.balance))
        self.dp.add_handler(CommandHandler("long", self.long_order))
        self.dp.add_handler(CommandHandler("short", self.short_order))
        self.dp.add_handler(CommandHandler("roi", self.roi))
        self.dp.add_handler(CommandHandler("livetrade", self.livetrade))

    def send_telegram_message(self, message: str):
        """Send a message to the Telegram chat."""
        self.bot.send_message(chat_id=self.chat_id, text=message)

if __name__ == "__main__":
    tele = TeleComm()
    tele.updater.start_polling()
    tele.updater.idle()