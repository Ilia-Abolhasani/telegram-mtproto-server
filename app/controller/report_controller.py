from app.Context import Context


class ReportController:
    def __init__(self):
        self.context = Context()

    def post_speed(self, agent_id, reports):
        self.context.add_bach_speed_report(agent_id, reports)

    def post_ping(self, agent_id, reports):
        self.context.add_bach_ping_report(agent_id, reports)
