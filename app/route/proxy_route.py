from flask import Blueprint, jsonify
from app.controller.proxy_controller import ProxyController

blueprint = Blueprint('proxy', __name__)
controller = ProxyController()


@blueprint.route('/speed_test', methods=['GET'])
def get_speed_test():
    agent_id = 1
    result = controller.get_proxies_speed_test(agent_id)
    return jsonify(result)

@blueprint.route('/ping', methods=['GET'])
def get_ping():
    agent_id = 1
    result = controller.get_proxies_ping(agent_id)
    return jsonify(result)


@blueprint.route('/', methods=['GET'])
def home():
    return "This is the home route"
