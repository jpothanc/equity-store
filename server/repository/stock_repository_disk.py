import json

from injector import inject, Injector

from config.config_provider import ConfigProvider
from repository.stock_repository import StockRepository


class StockRepositoryDisk(StockRepository):

    @inject
    def __init__(self, injector: Injector):
        self.config_provider = injector.get(ConfigProvider)

    def get_stock(self, ric_code):
        file_path = self.config_provider.get('disk_data')
        print(f"Path: {file_path}")
        # return f"Disk: {ric_code}"
        try:
            with open(file_path, 'r') as file:
                stocks = json.load(file)
                print(f"Path: loaded")
                return stocks
        except FileNotFoundError:
            return f"File not found: {file_path}"
        except Exception as e:
            return f"Error: {e}"

    def get_stocks(self):
        pass
