from flask import Blueprint, jsonify
from app.controller.agent_controller import AgentController

blueprint = Blueprint('agent', __name__)
controller = AgentController()


@blueprint.route('/')
def get_agents():
    agents = controller.get_agents()
    return jsonify(agents)

# More routes and handlers can be defined similarly
