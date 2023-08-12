from timeout_decorator import timeout
import time
import telegram.client as client
import os
import sys
sys.path.append("./utils/")
from DotDict import DotDict

# def file_handler(update):
#     local_file = update.get('file', {}).get('local', {})
#     is_downloading_completed = local_file.get('is_downloading_completed')

#     if is_downloading_completed:
#         local_path = local_file['path']
     
class TelegramAPI:
    def __init__(self):
       api_id = int(os.getenv("telegram_app_id"))
       api_hash = os.getenv("telegram_app_hash")
       phone = os.getenv("telegram_phone")
       self.tg = client.Telegram(
           api_id=api_id,
           api_hash=api_hash,
           phone=phone,
           database_encryption_key='changekey123',
           files_directory='../td/'
       )
       self.tg.login()
       #self.tg.add_update_handler('updateFile', file_handler)

    def __del__(self):
        self.tg.stop()

    def _call(self, method_name, params):
        result = self.tg.call_method(
            method_name=method_name,
            params=params
        )
        result.wait()
        return result

    def _dot(self, dict):
        return DotDict(dict)

    def add_proxy(self, server, port, secret):
        return self._call("addProxy", {
            'server': server,
            'port': port,
            'enable': True,
            'type': {
                '@type': 'proxyTypeMtproto',
                'secret': secret
            }
        })

    def enable_proxy(self, proxy_id):
        return self._call("enableProxy", {
            'proxy_id': proxy_id
        })

    def remove_proxy(self, proxy_id):
        return self._call("removeProxy", {
            'proxy_id': proxy_id
        })

    def ping_proxy(self, proxy_id):
        return self._call("pingProxy'", {
            'proxy_id': proxy_id
        })

    def get_proxies(self):
        result = self._call("getProxies", {})
        proxies = result.update['proxies']
        output = []
        for proxy in proxies:
            output.append(self._dot(proxy))
        return output

    def remove_all_proxies(self):
        proxies = self.get_proxies()
        for proxy in proxies:
            self.remove_proxy(proxy.id)

    def search_public_chat(self, username):
        result = self._call("searchPublicChat", {
            'username': username
        })
        return result.update['id']

    def channel_hsitory(self, chat_id, limit, from_message_id, offset, only_local):
        result = self._call("getChatHistory", {
            'chat_id': chat_id,
            'limit': limit,
            'from_message_id': from_message_id,
            'offset': offset,
            'only_local': only_local,
        })
        return result

    @timeout(5)  
    def download_file(self, file_id, priority):
        start_time = time.time()
        result = self._call("downloadFile", {
            'file_id': file_id,
            'priority': priority,
            'synchronous': True
        })
        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Elapsed time: {elapsed_time:.6f} seconds")
        return result

    def idle(self):
        self.tg.idle()

    def stop(self):
        self.tg.stop()
