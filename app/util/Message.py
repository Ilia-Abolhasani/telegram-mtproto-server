import app.util.Mtproto as Mtproto


def padding(text, num):
    text = str(text)
    l = len(text)
    for i in range(l, num):
        text = " " + text + " "
    return text


def create_star(ping, speed):
    num_star = 1
    if (speed > 1000 and ping < 200):
        num_star = 5
    elif (speed > 700 and ping < 200):
        num_star = 4
    elif (speed > 400 and ping < 300):
        num_star = 3
    elif (speed > 200 and ping < 400):
        num_star = 2
    return "⭐️" * num_star


def create_message(proxies, connect_num, total, channels_num):
    text = "لیست سریع‌ترین پروکسی‌های انتخاب شده توسط کاوشگر هوش مصنوعی"
    message = f"<b>{text}:</b>\n\n"

    for proxy in proxies:
        url = Mtproto.create_proxy_link(proxy.server, proxy.port, proxy.secret)

        speed = f"<b>speed:</b> {padding(proxy.average_speed // 1, 5)} kB/s"
        ping = f"<b>ping:</b> {padding(proxy.latest_ping // 1, 5)} ms"
        star = create_star(proxy.latest_ping, proxy.average_speed)
        proxy_info = f"<i><a href='{url}'>📶 Connect Proxy</a> {star}\nℹ️ {speed}| {ping}</i>\n"
        message += proxy_info + "\n"

    message += "<b>Database Status:</b>\n"
    message += f"🔗 Connected Proxies: {connect_num}\n"
    message += f"📊 Total Existing Proxies: {total}\n"
    message += f"📡 Number of Explored Proxy Channels: {channels_num}\n"
    message += "\n🆔 @mtprotoAI"
    return message
