import json
import logging

from flask import Flask, session
from flask_injector import FlaskInjector
from injector import singleton

from config.config_provider import ConfigProvider
from config.constants import FACTORY_FILE, CONFIG_FILE
from controllers.equity_controller import equity_api
from imports import EquityService, StockRepositoryDisk, StockRepository, StockRepositoryDB

def configure(binder):
    with open(FACTORY_FILE, 'r') as file:
        factory_config = json.load(file)

    for binding in factory_config.get('bindings'):
        binder.bind(
            eval(binding['service']),
            to=eval(binding['implementation']),
            scope=eval(binding['scope']))
    binder.bind(ConfigProvider, to=ConfigProvider(CONFIG_FILE), scope=singleton)


def create_app():
    equity_app = Flask(__name__)
    equity_app.register_blueprint(equity_api, url_prefix='/api/equity')
    flask_injector = FlaskInjector(app=equity_app, modules=[configure])
    return equity_app, flask_injector


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("equity-store.log"),
            logging.StreamHandler()])


if __name__ == '__main__':
    app, flask_injector = create_app()
    init_logging()
    config_provider =  flask_injector.injector.get(ConfigProvider)
    port = config_provider.get('port') or 8001
    print(port)
    app.run(debug=True, host='0.0.0.0', port=port)
