from abc import abstractmethod


class StockRepository:
    def __init__(self):
        pass

    @abstractmethod
    def get_stock(self, ric_code):
        raise NotImplementedError

    @abstractmethod
    def get_stocks(self):
        raise NotImplementedError

