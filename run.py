from TelegramAPI import TelegramAPI

from dotenv import load_dotenv
load_dotenv()
client = TelegramAPI()
client.remove_all_proxies()





# client.add_proxy(
#     "crack.income.know.host.question.nod.bookcasestreet.quest",
#     443,
#     "7vQ1mpsyX_HR5QhN8OD3U3ttc24uY29t")
# proxy_id = client.get_proxies()[0].id
# client.enable_proxy(proxy_id)

channel_id = client.search_public_chat("ProxyMTProto")
result = client.channel_hsitory(channel_id, 100, 0, 0, True)
print(result.update['total_count'])
message_id = result.update['messages'][0]["id"]
result = client.channel_hsitory(channel_id, 100, message_id, 0, True)
print(result.update['total_count'])

urls = []
for message in result.update['messages']:    
    urls = [*urls, *extract_all_mtproto(message)]    
for url in set(urls):
    print(url)