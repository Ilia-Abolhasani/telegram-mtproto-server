import re
import json
from TelegramAPI import TelegramAPI

from dotenv import load_dotenv
load_dotenv()
client = TelegramAPI()
client.remove_all_proxies()

client.add_proxy(
     "e.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.l.zeit.yachts.",
     443,
     "7gAAAAAAAAAAAAAAAAAAAAB3ZWIuYmFsZS5pcg==")
proxy_id = client.get_proxies()[0].id
client.enable_proxy(proxy_id)

recived_messages, last_message_id = client.channel_hsitory("speed_test_channel", 100, None)
fileid = recived_messages[1]['content']['document']['document']['id']
print(client.speed_test(fileid))
# try:
#     client.download_file(fileid, 32)
# except TimeoutError:
#     print("Function took too long to execute and was timed out.")
# client.idle()
