from app.util.Mtproto import extract_all_mtproto, parse_proxy_link
from app.util.DotDict import DotDict
from app.cron import job_lock
from tqdm import tqdm


def start(context, telegram_api):
    global job_lock
    with job_lock:
        channels = context.get_all_channel()
        for channel in tqdm(channels):
            try:
                if (not channel.chat_id):
                    if (channel.is_public):
                        chat_id = telegram_api.search_public_chat(
                            channel.username)
                        if (not chat_id):
                            raise Exception(
                                f"public channel username '{channel.username}' not found!")
                        channel.chat_id = chat_id
                    else:
                        raise Exception("private channel without chat_id!")

                messages, last_message_id = telegram_api.channel_history(
                    channel.chat_id, 500, channel.last_id)
                proxy_linkes = []
                # get messages
                for message in messages:
                    for link in extract_all_mtproto(message):
                        proxy_linkes.append(link)
                proxy_linkes = list(set(proxy_linkes))
                proxies = []
                for link in proxy_linkes:
                    server, port, secret = parse_proxy_link(link)
                    if (len(server) > 255 or len(secret) > 255):
                        continue
                    proxies.append(
                        DotDict(
                            {
                                "server": server,
                                "port": port,
                                "secret": secret
                            }
                        )
                    )
                context.add_proxies_of_channel(proxies,
                                               channel,
                                               last_message_id)
            except Exception as e:
                print("Error in channel: " + channel)
                print("Error:", e)
