from app.util.Message import create_message
from app.cron import job_lock
from app.config.config import Config
import time


def start(context, bot_api):
    global job_lock
    with job_lock:
        start_time = time.time()
        proxies = context.get_top_proxies(Config.message_limit_proxy)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'get_top_proxies elapsed time: {elapsed_time}')
        connect_num = context.count_connect_proxies()
        total = context.count_total_proxies()
        channels_num = context.count_channels()
        message = create_message(proxies, connect_num, total, channels_num)
        result = bot_api.send_message(message)
        message_id = result.message_id
        context.add_or_update_setting("last_sent_message_id", message_id)
