from flask import request, g as data


class ChannelController:
    def __init__(self):
        pass

    def get_all(self):
        return data.context.get_all_channel()
