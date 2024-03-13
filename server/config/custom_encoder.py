import json
from dataclasses import asdict

from models.stock_info import StockInfo


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StockInfo):
            return asdict(obj)  # Convert the data class instance to a dict
        return super().default(obj)  # Fallback for other types
