from flask_restx import Resource, Namespace

from models.namespaces import eq_ns_namespace
from models.parsers import eq_exchange_parser
from services.authenticate import requires_auth
from services.equity_service import EquityService

# These namespaces are used to group the routes together and will have to be defined in the
# same class where the routes are defined
eq_ex_ns = eq_ns_namespace()
@eq_ex_ns.route('/exchange')
class EquityExchange(Resource):
    @eq_ex_ns.doc('get_equity_exchange')
    @eq_ex_ns.response(201, 'equity exchange details')
    @eq_ex_ns.response(400, 'Internal Error')
    @eq_ex_ns.response(500, 'Internal Server Error')
    @eq_ex_ns.expect(eq_exchange_parser)  #
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

    @eq_ex_ns.expect(eq_exchange_parser)
    @requires_auth
    def post(self):
        """Create a new equity exchange entry"""
        args = eq_exchange_parser.parse_args()
        exchange = args.get('exchange')
        # Here you would write code to save data to your database
        return {'message': 'Equity exchange created successfully', 'data': exchange}, 201

    @eq_ex_ns.expect(eq_exchange_parser)
    @requires_auth
    def put(self):
        """ Update an existing equity exchange entry by its ID"""
        args = eq_exchange_parser.parse_args()
        exchange = args.get('exchange')
        # Here you would find the exchange in the database and update its fields
        return {'message': 'Exchange updated successfully', 'data': exchange}, 200

    @eq_ex_ns.expect(eq_exchange_parser)
    @requires_auth
    def delete(self, exchange_id):
        """Delete an equity exchange entry by its ID"""
        args = eq_exchange_parser.parse_args()
        exchange = args.get('exchange')
        # Here you would find the exchange in the database and delete it
        return {'message': 'Exchange deleted successfully', 'data': exchange }, 204