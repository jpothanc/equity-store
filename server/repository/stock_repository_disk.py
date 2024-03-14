import json
import logging
import os
import threading
import time

from injector import inject, Injector
from config.config_provider import ConfigProvider
from repository.stock_repository import StockRepository


class StockRepositoryDisk(StockRepository):
    DATA_DIR = "data"
    @inject
    def __init__(self, injector: Injector):
        super().__init__()
        self.config_provider = injector.get(ConfigProvider)

    def load_exchange(self, exchange):
        file_path = os.path.join(self.DATA_DIR, f"{exchange}-stocks.json".lower())
        logging.info(f"load_exchange {exchange} Current thread ID: {threading.current_thread().ident}")
        start_time = time.time()
        try:
            with open(file_path, 'r') as file:
                stocks = json.load(file)
                self.cache_exchange[exchange] = stocks
                self.index_stocks(stocks)

            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            logging.info(f"Loaded {exchange} stocks: {len(stocks)} in ({elapsed_time:.2f} ms)")

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


