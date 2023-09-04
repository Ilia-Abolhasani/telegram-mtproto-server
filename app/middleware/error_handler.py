import traceback
from flask import Flask
from flask import jsonify
from app.util.LoggerBot import LoggerBot
logger_bot = LoggerBot()


def register_error_handlers(app):
    app.register_error_handler(404, _access_denied_error)
    app.register_error_handler(404, _not_found_error)
    app.register_error_handler(500, _internal_error)
    app.register_error_handler(
        Exception, _handle_global_exception)


def _access_denied_error(error):
    return jsonify({"error": "Access denied."}), 403


def _not_found_error(error):
    return jsonify({"error": "Page not found."}), 404


def _internal_error(error):
    traceback_str = traceback.format_exc()
    error_message = f"Internal server error: {str(error)}"
    message = f"{error_message}\n\n{traceback_str}"
    logger_bot.send(message)
    return jsonify({"error": "Internal server error"}), 500


def _handle_global_exception(error):
    traceback_str = traceback.format_exc()
    error_message = f"An error occurred: {str(error)}"
    message = f"{error_message}\n\n{traceback_str}"
    logger_bot.send(message)
    return jsonify("An error occurred"), 500
