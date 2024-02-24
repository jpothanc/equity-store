from flask import Blueprint, request, jsonify

from services.equity_service import EquityService

equity_api = Blueprint('equity_api', __name__)


@equity_api.route('/health', methods=['GET'])
def health():
    return create_response({'health': 'healthy'})


@equity_api.route('/', methods=['GET'])
def get_equity(eq_service: EquityService):
    ric_code = request.args.get('ric_code')
    return eq_service.get_equity(ric_code)


def create_response(data, status_code=200, headers=None):
    response = jsonify(data)
    response.status_code = status_code

    if headers:
        for key, value in headers.items():
            response.headers[key] = value

    return response
