from flask import jsonify, Blueprint

# Create a Blueprint for the health check endpoints
health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'UP'}), 200