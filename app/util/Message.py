import app.util.Mtproto as Mtproto


def create_message(proxies):
    message = """پیام ویرایش شد"""
    for proxy in proxies:
        url = Mtproto.create_proxy_link(proxy.server, proxy.port, proxy.secret)
        message += f"\n<a href='{url}'>Proxy</a>"
    return message
