from context import session
from model.proxy import Proxy

def main():
    new_proxy = Proxy(server='proxy.example.com', port=8080, secret='mysecret')
    session.add(new_proxy)
    session.commit()

    proxies = session.query(Proxy).all()
    for proxy in proxies:
        print(proxy.server, proxy.port, proxy.secret)

if __name__ == "__main__":
    main()
