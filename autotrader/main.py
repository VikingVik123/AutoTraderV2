import os
import json
from autotrader.data.get_history import Get_history
from autotrader.dataframes.data import Price2DataFrame
from autotrader.strategies.default import DefaultStrategy
from autotrader.indicators.technical import Technical_Indicators
from autotrader.portfolio.monitoring import MonitorTrades
from autotrader.portfolio.account import SimAccount
from autotrader.engines.simengine import TradingEngine
from autotrader.telegr.tele import TeleComm


config_path = os.path.join(os.path.dirname(__file__), ".", "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

token = config["telegram"]["token"]
chat_id = config["telegram"]["chatId"]

if __name__ == "__main__":
    engine = TradingEngine()
    bot = TeleComm(token, chat_id, engine.account, engine.monitor)
    
    # Run the engine in a separate thread
    import threading
    engine_thread = threading.Thread(target=engine.run)
    engine_thread.daemon = True  # This ensures the thread will close when the main program exits
    engine_thread.start()
    
    # Run the Telegram bot in the main thread
    bot.run()