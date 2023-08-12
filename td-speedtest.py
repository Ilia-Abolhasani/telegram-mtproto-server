import os
import sys
from dotenv import load_dotenv
sys.path.append("../python-telegram/")
from telegram.client import Telegram
sys.path.append("../python-telegram/examples")
from utils import setup_logging


def main():
    load_dotenv()

    api_id = int(os.getenv("telegram_app_id"))
    api_hash = os.getenv("telegram_app_hash")
    phone = os.getenv("telegram_phone")
    channel_username = "speed_test_channel"#"ProxyHagh"
    limit = 5

    proxy_type = {
        '@type': 'proxyTypeMtproto',
        'secret': "50727642794d696c6164456d61646900"
    }

    tg = Telegram(
        api_id=api_id,
        api_hash=api_hash,
        phone=phone,
        database_encryption_key='changekey123',
        files_directory='../td/',
        #proxy_server="37.156.146.166",
        #proxy_port=4433,
        #proxy_type=proxy_type,
    )
    tg.login()    

    # result = tg.search_public_chat(channel_username)
    # result.wait()
    # #print(result.update)
    # id = result.update["id"]

    # result = tg.get_chat_history(chat_id=id, limit=limit)
    # result.wait()
    # print(result.update)

    
    # result = tg.get_message(chat_id=-1001419233283, message_id=108003328)
    # result.wait()
    # print(result.update)

    # def file_handler(update):
    #     local_file = update.get('file', {}).get('local', {})
    #     is_downloading_completed = local_file.get('is_downloading_completed')        
    #     if is_downloading_completed:
    #         local_path = local_file['path']
    # tg.add_update_handler('updateFile', file_handler)

    # file_id = 2219
    # result = tg.call_method('downloadFile', params={'file_id': file_id, 'priority': 1})
    # result.wait()
    # print(result)

    # result = tg.get_proxies()
    # result.wait()
    # print(result.update)

    # result = tg.enable_proxy(4)
    # result.wait()
    # print(result.update)    


    # result = tg.get_proxies()
    # result.wait()
    # print(result.update)

    # result = tg.ping_proxies(2)
    # result.wait()
    # print(result.update)

    # result = tg.remove_proxy(4)
    # result.wait()
    # print(result.update)       
    
    # result = tg.enable_proxy(4)
    # result.wait()
    # print(result.update)    


    
    def new_message_handler(update):
        message_content = update['message']['content'].get('text', {})
        message_text = message_content.get('text', '').lower()
        is_outgoing = update['message']['is_outgoing']

        # if not is_outgoing and message_text == 'ping':
        if True:
            chat_id = update['message']['chat_id']
            print(f'Ping has been received from {chat_id}')
            # tg.send_message(
            # chat_id=chat_id,
            # text='pong',
            # )

    tg.add_message_handler(new_message_handler)
    tg.idle()

    tg.stop()

if __name__ == '__main__':
    # setup_logging(level=logging.INFO)
    main()
