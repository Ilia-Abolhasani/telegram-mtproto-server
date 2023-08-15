from flask import Flask
from flask import jsonify


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
    return jsonify({"error": "Internal server error"}), 500


def _handle_global_exception(error):
    # todo email the error
    return jsonify({"error": "An error occurred"}), 500
