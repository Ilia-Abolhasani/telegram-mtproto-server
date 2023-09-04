import os
from pytgbot import Bot
import logging
from app.config.config import Config
logging.basicConfig(level=logging.DEBUG)


class LoggerBot:
    def __init__(self):
        self.bot = Bot(Config.loggger_bot_api_key)
        self.chat = Config.loggger_bot_chat_id

    def send(self, text, parse_mode="HTML"):
        result = self.bot.send_message(self.chat, text, parse_mode)
        return result
