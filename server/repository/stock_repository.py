from abc import abstractmethod


class StockRepository:
    def __init__(self):
        self.cache_exchange = {}
        self.cache_stock_code = {}

    @abstractmethod
    def load_exchange(self, exchange):
        pass

    @abstractmethod
    def get_stock(self, ric_code):
        raise NotImplementedError

    @abstractmethod
    def get_exchange(self, exchange):
        raise NotImplementedError

