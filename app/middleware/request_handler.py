from flask import request, g as data
from app.Context import Context


def request_handler_middleware():
    data.context = Context()
    print("Middleware: Request received from:", request.remote_addr)
