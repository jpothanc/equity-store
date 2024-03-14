from flask import g
from flask_restx import Resource

from models.models import stock_info_model
from internal.namespaces import eq_ns_namespace
from internal.parsers import eq_parser
from services.authentication_service import requires_auth
from services.equity_service import EquityService

# These namespaces will have to be defined in the same class where the routes are defined
eq_ns = eq_ns_namespace()
stock_info = stock_info_model(eq_ns)
@eq_ns.route('')
class Equity(Resource):
    @eq_ns.doc('get_equity')
    @eq_ns.response(201, 'equity details')
    @eq_ns.response(400, 'Internal Error')
    @eq_ns.response(500, 'Internal Server Error')
    @eq_ns.expect(eq_parser)
    def get(self):
        """Get equity"""
        try:
            args = eq_parser.parse_args()
            code = args.get('product_code')
            if not code:
                return {"message": "Product code is required."}, 400
            eq_service = g.flask_injector.injector.get(EquityService)
            equity =  eq_service.get_equity(code)
            if equity is None:
                return {"message": "Equity not found"}, 404
            return equity,200
        except Exception as e:
            return {"message": "Internal Server Error", "error": str(e)}, 500

    @eq_ns.expect(stock_info)
    @requires_auth
    def post(self):
        """Create a new equity """
        return {"message": "Stock info received", "data": eq_ns.payload}, 201

    @eq_ns.expect(stock_info)
    @requires_auth
    def delete(self):
        """Delete a equity """
        return {"message": "Stock info to delete received", "data": eq_ns.payload}, 201

