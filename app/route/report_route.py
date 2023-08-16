import json
from flask import Blueprint, jsonify, request
from app.controller.report_controller import ReportController

blueprint = Blueprint('report', __name__)
controller = ReportController()


@blueprint.route('/', methods=['POST'])
def post_reports():
    data = request.data
    decoded_data = data.decode('utf-8')  
    json_object = json.loads(decoded_data) 
    return json_object
