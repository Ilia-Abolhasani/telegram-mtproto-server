from app.util.Message import create_message


def start(job_lock, context, bot_api):
    with job_lock:
        proxies = context.get_top_proxies(10)
        message = create_message(proxies)
        result = bot_api.send_message(message)
        message_id = result.message_id
        context.add_or_update_setting("last_sent_message_id", message_id)
