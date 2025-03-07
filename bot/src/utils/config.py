import json
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, config_file="config.json"):
        """
        Handles loading and parsing of the config file
        """
        self.config = config_file
        self.settings = self.load_config()