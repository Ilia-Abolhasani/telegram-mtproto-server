from flask import Blueprint, jsonify
from app.controller.agent_controller import AgentController

blueprint = Blueprint('agent', __name__)
controller = AgentController()


@blueprint.route('/')
def get_agents():
    agent_id = 1
    result = controller.get_agent(agent_id)
    return jsonify(result)

