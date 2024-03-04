from flask import jsonify, g
from flask_restx import Namespace, Resource, reqparse
from services.equity_service import EquityService

eq_ns = Namespace('equity', description='Equity operations', path='/api/v1/equity')

parser_eq = reqparse.RequestParser()
parser_eq.add_argument('product_code', type=str, location='args', required=True, help='Equity to search for')

parser_eq_exchange = reqparse.RequestParser()
parser_eq_exchange.add_argument('exchange', type=str, location='args', required=True, help='Equity Exchange to search for')

@eq_ns.route('/')
class Equity(Resource):
    @eq_ns.doc('get_equity')
    @eq_ns.response(201, 'equity details')
    @eq_ns.response(400, 'Internal Error')
    @eq_ns.expect(parser_eq)  #
    def get(self):
        """Get equity"""
        args = parser_eq.parse_args()
        code = args.get('product_code')
        eq_service = g.flask_injector.injector.get(EquityService)
        return eq_service.get_equity(code), 201

@eq_ns.route('/exchange')
class EquityExchange(Resource):
    @eq_ns.doc('get_equity_exchange')
    @eq_ns.response(201, 'equity exchange details')
    @eq_ns.response(400, 'Internal Error')
    @eq_ns.expect(parser_eq_exchange)  #
    def get(self):
        """Get equity Exchange"""
        args = parser_eq_exchange.parse_args()
        exchange = args.get('exchange')
        eq_service = g.flask_injector.injector.get(EquityService)
        return eq_service.get_exchange(exchange), 201

def create_response(data, status_code=200, headers=None):
    response = jsonify(data)
    response.status_code = status_code

    if headers:
        for key, value in headers.items():
            response.headers[key] = value

    return response
