from repository.stock_repository import StockRepository



class StockRepositoryDB(StockRepository):
    def get_exchange(self, exchange):
        pass

    def load_exchange(self, exchange):
        pass

    def __init__(self):
        pass

    def get_stock(self, ric_code):
        return f"DB: {ric_code}"

    def get_stocks(self):
        pass