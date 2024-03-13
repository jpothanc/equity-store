import json
import logging
import os

from flask import Flask, session, g
from flask_injector import FlaskInjector, request
from injector import singleton
from config.config_provider import ConfigProvider
from config.constants import FACTORY_FILE, CONFIG_FILE
from controllers import error_handlers
from controllers.equity_controller import eq_ns
from controllers.equity_exchange_controller import eq_ex_ns

from controllers.health_controller import health_bp
from imports import EquityService, StockRepositoryDisk, StockRepository, StockRepositoryDB, DatabaseService, DbPostgresService,EncryptionService
from flask_restx import Api, Resource




def configure(binder):
    try:
        with open(FACTORY_FILE, 'r') as file:
            factory_config = json.load(file)

        for binding in factory_config.get('bindings'):
            binder.bind(
                eval(binding['service']),
                to=eval(binding['implementation']),
                scope=eval(binding['scope']))
        binder.bind(ConfigProvider, to=ConfigProvider(CONFIG_FILE), scope=singleton)

    except FileNotFoundError:
        print(f"File not found: {FACTORY_FILE}")
    except Exception as e:
        print(f"Error: {e}")

def create_app():
    main_app = Flask(__name__, static_folder = 'static/dist', template_folder= 'static/dist')
    return main_app, FlaskInjector(app=main_app, modules=[configure])

app, flask_injector = create_app()
api = Api(app, version='1.0', title='Equity Store API', description='Equity Store API')

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("equity-store.log"),
            logging.StreamHandler()])

def register_blueprints_and_api():
    api.add_namespace(eq_ns)
    api.add_namespace(eq_ex_ns)
    app.register_blueprint(health_bp)

def register_error_handlers():
    app.register_error_handler(404, error_handlers.not_found)
    app.register_error_handler(500, error_handlers.internal_server_error)

@app.before_request
def before_request():
    g.flask_injector = flask_injector
    g.api = api


if __name__ == '__main__':
    init_logging()
    config_provider =  flask_injector.injector.get(ConfigProvider)
    encrypt_service = flask_injector.injector.get(EncryptionService)
    equity_service = flask_injector.injector.get(EquityService)
    register_error_handlers()
    register_blueprints_and_api()
    equity_service.load_exchanges()
    port = config_provider.get('port') or 8001
    print(port)

    app.run(debug=True, host='0.0.0.0', port=port)
