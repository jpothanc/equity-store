from flask_restx import reqparse

from models.stock_info import StockInfo

eq_parser = reqparse.RequestParser()
eq_parser.add_argument('product_code', type=str, location='args', required=True, help='Equity to search for')

eq_exchange_parser = reqparse.RequestParser()
eq_exchange_parser.add_argument('exchange_code', type=str, location='args', required=True, help='Equity Exchange to search for')