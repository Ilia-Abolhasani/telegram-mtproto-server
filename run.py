from app import app
from app.middleware import error_handler

if __name__ == '__main__':
    error_handler.register_error_handlers(app)
    app.run(debug=False)
