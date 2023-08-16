from app.util.Mtproto import extract_all_mtproto, parse_proxy_link


def start(context, telegram_api):
    channels = context.get_all_channel()
    for channel in channels:
        try:
            messages, last_message_id = telegram_api.channel_hsitory(
                channel.username, 100, channel.last_id)
            proxy_linkes = []
            # get messages
            for message in messages:
                for link in extract_all_mtproto(message):
                    proxy_linkes.append(link)
            proxy_linkes = list(set(proxy_linkes))
            for link in proxy_linkes:
                server, port, secret = parse_proxy_link(link)
                context.add_proxy(server, port, secret, False)
            channel.last_id = last_message_id
            context.session.commit()
        except Exception as e:
            context.session.rollback()
            print("Error:", e)
