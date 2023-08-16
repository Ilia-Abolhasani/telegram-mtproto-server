from app.route.agent_route import blueprint as agent_bp
from app.route.channel_route import blueprint as channel_bp
from app.route.proxy_route import blueprint as proxy_bp
from app.route.report_route import blueprint as report_bp
from flask import Blueprint

route_bp = Blueprint('route', __name__)

route_bp.register_blueprint(agent_bp, url_prefix='/api/agent')
route_bp.register_blueprint(channel_bp, url_prefix='/api/channel')
route_bp.register_blueprint(proxy_bp, url_prefix='/api/proxy')
route_bp.register_blueprint(report_bp, url_prefix='/api/report')
