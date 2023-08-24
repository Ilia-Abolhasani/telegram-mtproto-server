from app.Context import Context


class ProxyController:
    def __init__(self):
        self.context = Context()

    def get_proxies_ping(self, agent_id, disconnect):
        proxies = self.context.get_proxy_ping(agent_id, disconnect)
        result = []
        for proxy in proxies:
            result.append(proxy.to_json())
        return {"result": result}

    def get_proxies_speed_test(self, agent_id):
        proxies = self.context.get_proxy_speed_tests(agent_id)
        result = []
        for proxy in proxies:
            result.append(proxy.to_json())
        return {"result": result}
