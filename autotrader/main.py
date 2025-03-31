import os
import json
from autotrader.data.get_history import Get_history
from autotrader.dataframes.data import Price2DataFrame
from autotrader.strategies.default import DefaultStrategy
from autotrader.indicators.technical import Technical_Indicators
from autotrader.portfolio.monitoring import MonitorTrades
from autotrader.portfolio.account import SimAccount
from autotrader.engines.simengine import TradingEngine
from autotrader.telegram.tele import TeleComm


config_path = os.path.join(os.path.dirname(__file__), ".", "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

token = config["telegram"]["token"]
chat_id = config["telegram"]["chatId"]

if __name__ == "main":
    #tele = TeleComm(token, chat_id)
    #tele.run()
    engine = TradingEngine()
    engine.run(interval=60)
