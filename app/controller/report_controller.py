from app.Context import Context


class ReportController:
    def __init__(self):
        self.context = Context()

    def post_reports(self, agent_id, report_list):
        batch = 64
        proxies = self.context.get_proxy_ping(agent_id, batch)
        result = []
        for proxy in proxies:
            result.append(proxy.to_json())
        return result