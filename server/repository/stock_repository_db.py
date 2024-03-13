import json
from dataclasses import asdict

from injector import inject, Injector

from config.config_provider import ConfigProvider
from config.custom_encoder import CustomEncoder
from models.stock_info import StockInfo
from repository.stock_repository import StockRepository
from services.database_service import DatabaseService
from services.db_postgres_service import DbPostgresService


class StockRepositoryDB(StockRepository):
    @inject
    def __init__(self, injector: Injector):
        super().__init__()
        self.database_service =  injector.get(DatabaseService)
        self.config_provider = injector.get(ConfigProvider)


    def load_exchange(self, exchange):
        connection_string =  self.config_provider.data["db"]["connection_string"]
        col_names, rows = self.database_service.query(connection_string, f"SELECT stock_name, primary_exchange, product_code, lot_size,  currency, day_20_average_volume, day_30_average_volume FROM equity WHERE primary_exchange = '{exchange}'", )

        stocks = [
            StockInfo(*row)  # Unpack each row directly into the StockInfo constructor
            for row in rows
        ]
        stocks_dict_list = [stock.to_dict() for stock in stocks]
        print(stocks_dict_list)
        self.cache_exchange[exchange] = stocks_dict_list
        self.index_stocks(stocks_dict_list)

    def index_stocks(self, stocks):
        for stock in stocks:
            print(f"stock: {stock}")
            self.cache_stock_code[stock["product_code"]] = stock

    def get_exchange(self, exchange):
        return self.cache_exchange.get(exchange)

    def get_stock(self, product_code):
        return self.cache_stock_code.get(product_code)