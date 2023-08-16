from app.Context import Context


class AgentController:
    def __init__(self):
        self.context = Context()

    def get_agent(self, agent_id):        
        agent = self.context.get_agent(agent_id)                
        if(agent):
            agent = agent.to_json()                            
            del agent['encrypted_key']
            return agent
        return None
