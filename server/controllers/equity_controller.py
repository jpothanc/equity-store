from flask import g
from flask_restx import Namespace, Resource, reqparse
from models.parsers import eq_parser, eq_exchange_parser
from services.equity_service import EquityService

eq_ns = Namespace('equity', description='Equity operations', path='/api/v1/equity')

@eq_ns.route('/')
class Equity(Resource):
    @eq_ns.doc('get_equity')
    @eq_ns.response(201, 'equity details')
    @eq_ns.response(400, 'Internal Error')
    @eq_ns.response(500, 'Internal Server Error')
    @eq_ns.expect(eq_parser)  #
    def get(self):
        """Get equity"""
        try:
            args = eq_parser.parse_args()
            code = args.get('product_code')
            if not code:
                return {"message": "Product code is required."}, 400
            eq_service = g.flask_injector.injector.get(EquityService)
            equity =  eq_service.get_equity(code), 201
            if equity is None:
                return {"message": "Equity not found"}, 404
            return equity
        except Exception as e:
            return {"message": "Internal Server Error", "error": str(e)}, 500

@eq_ns.route('/exchange')
class EquityExchange(Resource):
    @eq_ns.doc('get_equity_exchange')
    @eq_ns.response(201, 'equity exchange details')
    @eq_ns.response(400, 'Internal Error')
    @eq_ns.response(500, 'Internal Server Error')
    @eq_ns.expect(eq_exchange_parser)  #
    def get(self):
        """Get equity Exchange"""
        try:
            args = eq_exchange_parser.parse_args()
            exchange = args.get('exchange')
            if not exchange:
                return {"message": "Exchange is required."}, 400
            eq_service = g.flask_injector.injector.get(EquityService)
            exchange =  eq_service.get_exchange(exchange), 201
            if exchange is None:
                return {"message": "Exchange not found"}, 404
            return exchange
        except Exception as e:
            return {"message": "Internal Server Error", "error": str(e)}, 500

