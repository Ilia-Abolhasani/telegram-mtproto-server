from app.util.LoggerBot import LoggerBot


class LogController:
    def __init__(self):
        self.logger_bot = LoggerBot()

    def send_log(self, agent_id, message, parse_mode="HTML"):
        message = f"Message from agent: {agent_id}:\n" + message
        return self.logger_bot.send(message, parse_mode)
