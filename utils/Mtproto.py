import re
import json
from urllib.parse import urlparse, parse_qs

def parse_proxy_link(proxy_link):
    pass
    #return server, port, secret


def is_valid_mtproto_link(link): # todo
    parsed_url = urlparse(link)
    required_params = ['server', 'port', 'secret']

    if parsed_url.scheme != 'https' or parsed_url.netloc != 't.me' or parsed_url.path != '/proxy':
        return False

    query_params = parse_qs(parsed_url.query)
    if len(query_params) != len(required_params):
        return False

    if not all(key in query_params for key in required_params):
        return False

    if not query_params['server'] or not query_params['port'] or not query_params['secret'] or not query_params['port'][0].isdigit():
        return False

    return True

def extract_all_mtproto(message):
    ulrs = []
    json_string = json.dumps(message, indent = 4) 
    urls = re.findall(r'"url": "https://t.me/proxy\?([^"]+)"', json_string)
    for url in urls:
        decoded_url = re.sub(r'%([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), url)        
        ulrs.append(decoded_url)                
    return ulrs
