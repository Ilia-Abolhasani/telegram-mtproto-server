import sys
import logging
from dotenv import load_dotenv
from flask import Flask
from app.cron.cron_manager import setup_cron_jobs
from app.Context import Context
from app.middleware.request_handler import request_handler_middleware
from app.route import route_bp  # Import the blueprint
from app.util.TelegramAPI import TelegramAPI
from app.util.BotAPI import BotAPI

load_dotenv()

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Uncaught')


def custom_excepthook(exctype, value, traceback):
    logger.error("Uncaught error.", exc_info=(exctype, value, traceback))


sys.excepthook = custom_excepthook

app = Flask(__name__)

# Register your route blueprint
app.register_blueprint(route_bp)

# Set up cron jobs
# setup_cron_jobs()

# Register request handler middleware
app.before_request(request_handler_middleware)

# Initialize
context = Context()
telegram_api = TelegramAPI()
bot_api = BotAPI()

setup_cron_jobs(context, telegram_api, bot_api)
