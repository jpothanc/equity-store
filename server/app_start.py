import logging
import os

from internal import error_handlers
from controllers.equity_controller import eq_ns
from controllers.equity_exchange_controller import eq_ex_ns
from controllers.health_controller import health_bp


def init_app(app,api,**kwargs):

    init_logging(kwargs.get('log_path'))
    register_error_handlers(app)
    register_blueprints_and_api(app,api)
"""
Initialize logging
"""
def init_logging(log_path):
        os.makedirs(log_path, exist_ok=True)
        log_file = os.path.join(log_path, 'equity_store.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                #This handler outputs log messages to the console
                logging.StreamHandler()])
"""
Register blueprints and api
"""
def register_blueprints_and_api(app, api):
    api.add_namespace(eq_ns)
    api.add_namespace(eq_ex_ns)
    app.register_blueprint(health_bp, url_prefix='/api')

"""
Global error handlers
"""
def register_error_handlers(app):
    app.register_error_handler(404, error_handlers.not_found)
    app.register_error_handler(500, error_handlers.internal_server_error)