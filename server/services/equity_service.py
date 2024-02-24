from injector import Injector, inject

from repository.stock_repository import StockRepository
from repository.stock_repository_disk import StockRepositoryDisk


class EquityService:
    @inject
    def __init__(self, injector: Injector):
        self.stock_repository = injector.get(StockRepository)

    def get_equity(self, ric_code):
        return self.stock_repository.get_stock(ric_code)
