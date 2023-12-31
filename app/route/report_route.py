import json
from flask import Blueprint, jsonify, request
from app.controller.report_controller import ReportController

blueprint = Blueprint('report', __name__)
controller = ReportController()


@blueprint.route('/speed', methods=['POST'])
def post_speed(agent_id):
    data = request.data
    decoded_data = data.decode('utf-8')
    json_object = json.loads(decoded_data)
    reports = json_object['reports']
    controller.post_speed(agent_id, reports)
    return jsonify(True), 200


@blueprint.route('/ping', methods=['POST'])
def post_ping(agent_id):
    data = request.data
    decoded_data = data.decode('utf-8')
    json_object = json.loads(decoded_data)
    reports = json_object['reports']
    controller.post_ping(agent_id, reports)
    return jsonify(True), 200
