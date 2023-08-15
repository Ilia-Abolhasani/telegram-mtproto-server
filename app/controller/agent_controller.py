from app.Context import Context


class AgentController:
    def __init__(self):
        self.context = Context()

    def get_agents(self):
        return 1
        connection = self.context.get_connection()
        agents = connection.fetch_agents()
        return agents
