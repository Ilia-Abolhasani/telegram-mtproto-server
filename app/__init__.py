from flask import Flask
from app.api.agent_routes import agent_bp
from app.api.proxy_routes import proxy_bp
from app.cron.cron_manager import setup_cron_jobs

app = Flask(__name__)

# Register your API blueprints
app.register_blueprint(agent_bp, url_prefix='/api/agents')
app.register_blueprint(proxy_bp, url_prefix='/api/proxies')

# Set up cron jobs
setup_cron_jobs()

# You can also do other initialization tasks here if needed
# ...

if __name__ == '__main__':
    app.run(debug=True)
