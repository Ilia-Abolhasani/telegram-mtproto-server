import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    server_port = os.getenv("server_port")
    database_name = os.getenv("database_name")
    database_user = os.getenv("database_user")
    database_pass = os.getenv("database_pass")
    database_host = os.getenv("database_host")
    database_port = os.getenv("database_port")
    telegram_app_id = os.getenv("telegram_app_id")
    telegram_app_hash = os.getenv("telegram_app_hash")
    telegram_phone = os.getenv("telegram_phone")
    database_encryption_key = os.getenv("database_encryption_key")
    tdlib_directory = os.getenv("tdlib_directory")
    download_timeout = os.getenv("download_timeout")
    # main chanel bot
    bot_api_key = os.getenv("bot_api_key")
    bot_chat_id = os.getenv("bot_chat_id")
    # logger
    loggger_bot_api_key = os.getenv("loggger_bot_api_key")
    loggger_bot_chat_id = os.getenv("loggger_bot_chat_id")
    message_limit_proxy = 5
    max_ping_value = 10000
    exponential_decay = 0.9
    contribute_history = 5
    ping_score_weight = 0.6
    speed_score_weight = 0.4
