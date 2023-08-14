import os
from pytgbot import Bot
import logging
logging.basicConfig(level=logging.DEBUG)


class BotAPI:
    def __init__(self, chat):
        bot_api_key = os.getenv("bot_api_key")
        self.bot = Bot(bot_api_key)
        self.chat = chat

    def send_message(self, text):
        result = self.bot.send_message(self.chat, text)
        return result

    def edit_message_text(self, text, message_id):
        result = self.bot.edit_message_text(text, self.chat, message_id)
        return result

    def delete_message(self, message_id):
        result = self.bot.delete_message(self.chat, message_id)
        return result

    def pin_chat_message(self, message_id, disable_notification):
        result = self.bot.pin_chat_message(
            self.chat, message_id, disable_notification)
        return result

#
