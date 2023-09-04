import json
from flask import Blueprint, jsonify, request
from app.controller.log_controller import LogController

blueprint = Blueprint('lot', __name__)
controller = LogController()


@blueprint.route('/recive', methods=['POST'])
def post_log(agent_id):
    data = request.data
    decoded_data = data.decode('utf-8')
    json_object = json.loads(decoded_data)
    message = json_object['message']
    parse_mode = "HTML"
    if ("parse_mode" in json_object):
        parse_mode = json_object['parse_mode']
    result = controller.send_log(agent_id, message, parse_mode)
    return jsonify({"message_id": result.message_id}), 200


@blueprint.route('/message', methods=['PUT'])
def edit_message(agent_id):
    data = request.data
    decoded_data = data.decode('utf-8')
    json_object = json.loads(decoded_data)
    message = json_object['message']
    parse_mode = "HTML"
    message_id = int(request.args.get('message_id'))
    if ("parse_mode" in json_object):
        parse_mode = json_object['parse_mode']
    result = controller.edit_message(message, message_id, parse_mode)
    return jsonify({"message_id": result.message_id}), 200
