import json
import logging

from flask import Flask, session, g
from flask_injector import FlaskInjector
from injector import singleton
from config.config_provider import ConfigProvider
from config.constants import FACTORY_FILE, CONFIG_FILE
from controllers.app_controller import app_api
from controllers.equity_controller import eq_ns
from imports import EquityService, StockRepositoryDisk, StockRepository, StockRepositoryDB
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
api.add_namespace(eq_ns)

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("equity-store.log"),
            logging.StreamHandler()])

@app.before_request
def before_request():
    g.flask_injector = flask_injector


if __name__ == '__main__':
    init_logging()
    config_provider =  flask_injector.injector.get(ConfigProvider)
    equity_service = flask_injector.injector.get(EquityService)
    equity_service.load_exchanges()
    port = config_provider.get('port') or 8001
    print(port)
    app.run(debug=True, host='0.0.0.0', port=port)
