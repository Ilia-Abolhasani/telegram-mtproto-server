from app.Context import Context
from app.util.BotAPI import BotAPI
from app.config.config import Config


class BotController:
    def __init__(self):
        self.context = Context()
        self.bot_api = BotAPI(Config.bot_chat_id)

    def add_message(self, message, parse_mode="HTML"):
        return self.bot_api.send_message(message, parse_mode)

    def edit_message(self, message, message_id, parse_mode="HTML"):
        return self.bot_api.edit_message_text(message, message_id,  parse_mode)
