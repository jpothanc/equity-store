import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from injector import Injector, inject

from config.config_provider import ConfigProvider
from repository.stock_repository import StockRepository

class EquityService:
    @inject
    def __init__(self, injector: Injector):
        self.stock_repository = injector.get(StockRepository)
        self.config_provider = injector.get(ConfigProvider)

    def load_exchanges(self):
        stock_exchange_list = self.config_provider.get("preload_exchanges").split(",")
        # Use ThreadPoolExecutor to run in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.stock_repository.load_exchange, stock_exchange) for stock_exchange in
                       stock_exchange_list]
            # Optionally wait for all tasks to complete and handle their results
            for future in as_completed(futures):
                try:
                    result = future.result()
                    # Handle the result if needed
                except Exception as e:
                    # Handle exceptions from the task
                    print(f"Task generated an exception: {e}")

    def get_equity(self, ric_code):
        return self.stock_repository.get_stock(ric_code)
    def get_exchange(self, exchange):
        return self.stock_repository.get_exchange(exchange)