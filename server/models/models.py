
from flask_restx import fields, Model

"""
This class is used to define the model for the stock info which is required for swagger documentation
"""
def stock_info_model(namespace):
    return namespace.model('StockInfo', {
        'stock_name': fields.String(required=True, description='The name of the stock'),
        'primary_exchange': fields.String(required=True, description='The primary exchange where the stock is listed'),
        'product_code': fields.String(required=True, description='The product code of the stock'),
        'lot_size': fields.Integer(required=True, description='The lot size of the stock'),
        'currency': fields.String(required=True, description='The currency of the stock'),
        'day_20_average_volume': fields.Float(required=True, description='The 20-day average volume of the stock'),
        'day_30_average_volume': fields.Float(required=True, description='The 30-day average volume of the stock'),
    })
