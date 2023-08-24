from app.util.Message import create_message
from app.cron import job_lock


def start(context, bot_api):
    global job_lock
    with job_lock:
        setting = context.get_setting("last_sent_message_id")
        if not setting:
            return
        message_id = int(setting.value)

        proxies = context.get_top_proxies(10)
        message = create_message(proxies)

        result = bot_api.edit_message_text(message, message_id)
