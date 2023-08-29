from app.Context import Context


class ReportController:
    def __init__(self):
        self.context = Context()

    def post_speed(self, agent_id, reports):
        try:
            self.context.add_bach_speed_report(agent_id, reports)
        except Exception as error:
            print("Error:", error)
            self.context.session.rollback()
            raise error

    def post_ping(self, agent_id, reports):
        try:
            self.context.add_bach_ping_report(agent_id, reports)
        except Exception as error:
            print("Error:", error)
            self.context.session.rollback()
            raise error
