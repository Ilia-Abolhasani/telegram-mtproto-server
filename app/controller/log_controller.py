from app.util.BotAPI import BotAPI
from app.config.config import Config


class LogController:
    def __init__(self):
        self.logger_bot = BotAPI(Config.loggger_bot_api_key, Config.loggger_bot_chat_id)

    def send_log(self, agent_id, message):
        message = f"Message from agent: {agent_id}:\n" + message
        return self.logger_bot.send(message)
