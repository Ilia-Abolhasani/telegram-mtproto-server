import logging
from dotenv import load_dotenv
from flask import Flask
from app.cron.manager import start_jobs
from app.Context import Context
from app.middleware.request_handler import request_handler_middleware
from app.route import route_bp
from app.util.Telegram import Telegram
from app.util.BotAPI import BotAPI
from app.config.config import Config


logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Uncaught')


def custom_excepthook(exctype, value, traceback):
    logger.error("Uncaught error.", exc_info=(exctype, value, traceback))


# sys.excepthook = custom_excepthook

app = Flask(__name__)
app.register_blueprint(route_bp)
app.before_request(request_handler_middleware)

# Initialize
context = Context()
telegram_api = Telegram(
    Config.telegram_app_id,
    Config.telegram_app_hash,
    Config.telegram_phone,
    Config.database_encryption_key,
    Config.tdlib_directory,
    "212.118.37.178",
    9443,
    "ee4416004416004400441604416000441663646e2e79656b74616e65742e636f6d646c2e676f6f676c652e636f6d666172616B61762E636F6D160301020001000100000000000000000000000000000000"
)
# telegram_api.remove_all_proxies()
bot_api = BotAPI(Config.bot_chat_id)

start_jobs(context, telegram_api, bot_api)
