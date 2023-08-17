from app.Context import Context


class ReportController:
    def __init__(self):
        self.context = Context()

    def post_reports(self, agent_id, reports):
        self.context.add_reports(agent_id, reports)
