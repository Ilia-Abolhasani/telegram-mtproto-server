from app.route.proxy_route import blueprint as proxy_bp
from app.route.report_route import blueprint as report_bp
from flask import Blueprint

route_bp = Blueprint('route', __name__)

route_bp.register_blueprint(proxy_bp, url_prefix='/api/<int:agent_id>/proxy')
route_bp.register_blueprint(report_bp, url_prefix='/api/<int:agent_id>/report')
