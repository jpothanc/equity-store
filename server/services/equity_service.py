from injector import Injector, inject

from repository.stock_repository import StockRepository
from repository.stock_repository_disk import StockRepositoryDisk


class EquityService:
    @inject
    def __init__(self, injector: Injector):
        self.stock_repository = injector.get(StockRepository)

    def load_exchanges(self):
        stock_exchange_list = ["TSE","HKSE"]
        for stock_exchange in stock_exchange_list:
            print(f"Stock Exchange: {stock_exchange}")
            print(self.stock_repository.load_exchange(stock_exchange))

    def get_equity(self, ric_code):
        return self.stock_repository.get_stock(ric_code)
    def get_exchange(self, exchange):
        return self.stock_repository.get_exchange(exchange)