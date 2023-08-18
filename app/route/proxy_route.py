from flask import Blueprint, jsonify
from app.controller.proxy_controller import ProxyController

blueprint = Blueprint('proxy', __name__)
controller = ProxyController()


@blueprint.route('/speed_test', methods=['GET'])
def get_speed_test(agent_id):
    result = controller.get_proxies_speed_test(agent_id)
    result = jsonify(result)
    return result, 200


@blueprint.route('/ping', methods=['GET'])
def get_ping(agent_id):
    result = controller.get_proxies_ping(agent_id)
    result = jsonify(result)
    return result, 200
