import schedule
from Mtproto import extract_all_mtproto

def start(context, telegramAPI):
    def job():
        channels = context.get_all_channel()
        for channel in channels:
            try:
                messages, last_message_id = telegramAPI.channel_hsitory("speed_test_channel", 100, None)
                proxy_linkes = []                
                for message in messages:
                    for link in extract_all_mtproto(message):
                        proxy_linkes.append(link)                
                proxy_linkes = link(set(proxy_linkes))
                for proxy in proxy_linkes:
                    context.add_proxy()

            except Exception:
                print("error")
                pass

    schedule.every(10).minutes.do(job)