from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
import json

config_path = os.path.join(os.path.dirname(__file__), "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

token = config["token"]
chat_id = config["chatId"]



