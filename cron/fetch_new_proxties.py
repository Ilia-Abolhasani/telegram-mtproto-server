import time
import schedule
from utils.Mtproto import extract_all_mtproto, parse_proxy_link

async def job(context, telegramAPI):
    print('hit')
    return
    channels = context.get_all_channel()
    for channel in channels:
        try:
            messages, last_message_id = telegramAPI.channel_hsitory("speed_test_channel", 1000, channel.last_id)
            proxy_linkes = []                
            # get messages
            for message in messages:
                for link in extract_all_mtproto(message):
                    proxy_linkes.append(link)                
            proxy_linkes = link(set(proxy_linkes))
            for link in proxy_linkes:
                server, port, secret = parse_proxy_link(link)
                context.add_proxy(server, port, secret, False)
            channel.last_id = last_message_id
            context.session.commit()
        except Exception as e:
            context.session.rollback()
            print("Error:", e)                  

async def start(context, telegramAPI):    
    schedule.every(5).seconds.do(
        lambda: job(context, telegramAPI))
    while True:
        schedule.run_pending()
        time.sleep(1)