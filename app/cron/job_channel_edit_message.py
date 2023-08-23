from app.util.Message import create_message


def start(context, bot_api):
    setting = context.get_setting("last_sent_message_id")
    if not setting:
        return
    message_id = int(setting.value)

    proxies = context.get_top_proxies(10)
    message = create_message(proxies)

    result = bot_api.edit_message_text(message, message_id)
