from flask import abort, request, jsonify
from app.Context import Context


def request_handler_middleware():
    if (request.view_args):
        agent_id = request.view_args.get('agent_id')
        if agent_id != 1:
            response = jsonify({"error": "Access denied."})
            response.status_code = 403
            return response
