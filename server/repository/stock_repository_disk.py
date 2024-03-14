import json
import logging

from injector import inject, Injector
from config.config_provider import ConfigProvider
from repository.stock_repository import StockRepository


class StockRepositoryDisk(StockRepository):
    @inject
    def __init__(self, injector: Injector):
        super().__init__()
        self.config_provider = injector.get(ConfigProvider)

    def load_exchange(self, exchange):
        file_path = f"data\\{exchange}-stocks.json".lower()
        try:
            with open(file_path, 'r') as file:
                stocks = json.load(file)
                self.cache_exchange[exchange] = stocks
                self.index_stocks(stocks)
                logging.info(f"Loaded {exchange} stocks: {len(stocks)}")

        except FileNotFoundError:
            return f"File not found: {file_path}"
        except Exception as e:
            return f"Error: {e}"

    def index_stocks(self, stocks):
        for stock in stocks:
            self.cache_stock_code[stock['product_code']] = stock
    def get_exchange(self, exchange):
       return self.cache_exchange.get(exchange)
    def get_stock(self, product_code):
        return self.cache_stock_code.get(product_code)


