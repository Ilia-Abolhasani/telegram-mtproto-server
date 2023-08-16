from flask import Blueprint, jsonify
from app.controller.channel_controller import ChannelController

blueprint = Blueprint('channel', __name__)
controller = ChannelController()


@blueprint.route('/')
def get_channel():
    channel = controller.get_all()
    return jsonify(channel)

