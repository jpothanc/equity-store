import json

from flask_injector import request
from injector import Module, singleton

from config.config_provider import ConfigProvider
from internal.constants import FACTORY_FILE, CONFIG_FILE

# region registering the services
from repository.stock_repository import StockRepository
from repository.stock_repository_disk import StockRepositoryDisk
from repository.stock_repository_db import StockRepositoryDB
from services.equity_service import EquityService
from services.database_service import DatabaseService
from services.db_postgres_service import DbPostgresService
from services.encryption_service import EncryptionService
# endregion

"""
This class is used to bind the services to their implementations and scopes
Steps
1. Add the bindings to factory.json
2. Make sure the dependencies are added in the order of their dependencies
3. import the services and their implementations
"""
class DependencyInjectionModules(Module):
    def configure(self, binder):
        try:

            with open(FACTORY_FILE, 'r') as file:
                factory_config = json.load(file)

            for binding in factory_config.get('bindings'):
                binder.bind(
                    eval(binding['service']),
                    to=eval(binding['implementation']),
                    scope=eval(binding['scope']))
            binder.bind(ConfigProvider, to=ConfigProvider, scope=singleton)

        except FileNotFoundError:
            print(f"File not found: {FACTORY_FILE}")
        except Exception as e:
            print(f"Error Configuring Dependency Injection: {e}")