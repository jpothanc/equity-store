import logging
import threading
import time

from injector import inject, Injector
from config.config_provider import ConfigProvider
from models.stock_info import StockInfo
from repository.stock_repository import StockRepository
from services.database_service import DatabaseService

class StockRepositoryDB(StockRepository):
    @inject
    def __init__(self, injector: Injector):
        super().__init__()
        self.database_service =  injector.get(DatabaseService)
        self.config_provider = injector.get(ConfigProvider)


    def load_exchange(self, exchange):
        connection_string =  self.config_provider.get_connection_string(self.config_provider.get("data_source"))
        query = self.config_provider.get("exchange_query").format(exchange = exchange)
        logging.info(f"load_exchange {exchange} Current thread ID: {threading.current_thread().ident}")
        start_time = time.time()
        col_names, rows = self.database_service.query(connection_string, query)

        stocks = [
            StockInfo(*row)  # Unpack each row directly into the StockInfo constructor
            for row in rows
        ]
        stocks_dict_list = [stock.to_dict() for stock in stocks]

        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000
        logging.info(f"Loaded {exchange} stocks: {len(stocks)} in ({elapsed_time:.2f} ms)")

        self.cache_exchange[exchange] = stocks_dict_list
        self.index_stocks(stocks_dict_list)

    def index_stocks(self, stocks):
        for stock in stocks:
            self.cache_stock_code[stock["product_code"]] = stock

    def get_exchange(self, exchange):
        return self.cache_exchange.get(exchange)

    def get_stock(self, product_code):
        return self.cache_stock_code.get(product_code)