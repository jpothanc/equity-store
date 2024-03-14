from flask import Flask, g
from flask_injector import FlaskInjector
from app_start import init_app
from config.config_provider import ConfigProvider
from config.dependency_injection_modules import DependencyInjectionModules
from flask_restx import Api
from services.equity_service import EquityService

eq_app = Flask(__name__, static_folder ='static/dist', template_folder='static/dist')
eq_api = Api(eq_app, version='1.0', title='Equity Store API', description='Equity Store API')
flask_injector  = FlaskInjector(app=eq_app, modules=[DependencyInjectionModules()])

config_provider = flask_injector.injector.get(ConfigProvider)
config_provider.load('config.json')
init_app(eq_app, eq_api,log_path = config_provider.get('log_path'))

equity_service = flask_injector.injector.get(EquityService)
equity_service.load_exchanges()

@eq_app.before_request
def before_request():
    g.flask_injector = flask_injector
    g.api = eq_api

if __name__ == '__main__':
    port = config_provider.get('port') or 8001
    eq_app.run(debug=True, host='0.0.0.0', port=port)
