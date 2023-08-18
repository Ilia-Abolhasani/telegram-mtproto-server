from app import app
from app.middleware import error_handler

error_handler.register_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=False)
