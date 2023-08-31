from app.util.Message import create_message
from app.cron import job_lock
from app.config.config import Config


def start(context, bot_api):
    global job_lock
    with job_lock:
        setting = context.get_setting("last_sent_message_id")
        if not setting:
            return
        message_id = int(setting.value)

        proxies = context.get_top_proxies(Config.message_limit_proxy)
        connect_num = context.count_connect_proxies()
        total = context.count_total_proxies()
        channels_num = context.count_channels()
        message = create_message(proxies, connect_num, total, channels_num)

        result = bot_api.edit_message_text(message, message_id)
