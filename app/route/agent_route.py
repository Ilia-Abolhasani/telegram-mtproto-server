from flask import Blueprint, jsonify
from app.controller.agent_controller import AgentController

blueprint = Blueprint('agent', __name__)
controller = AgentController()


@blueprint.route('/config')
def get_agents():
    config = {
        "bach_size": 32,
        "time_out": 30
    }
    return jsonify(config)

