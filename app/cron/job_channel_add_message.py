from app.util.Message import create_message


def start(context, bot_api):
    proxies = context.get_top_proxies()
    message = create_message(proxies)
    result = bot_api.send_message(message)
    message_id = result.message_id
    context.add_or_update_setting("last_sent_message_id", message_id)
