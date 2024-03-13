import decimal
from dataclasses import dataclass
from pydantic import BaseModel
@dataclass
class StockInfo:
    stock_name: str
    primary_exchange: str
    product_code: str
    lot_size: int
    currency: str
    day_20_average_volume: float
    day_30_average_volume: float

    def to_dict(self):
        return {
            "stock_name": self.stock_name,
            "primary_exchange": self.primary_exchange,
            "product_code": self.product_code,
            "lot_size": self.lot_size,
            "currency": self.currency,
            "day_20_average_volume": self.day_20_average_volume,
            "day_30_average_volume": self.day_30_average_volume,
        }


