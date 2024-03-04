from flask import Blueprint, request, jsonify, render_template, send_from_directory
from flask_restx import Api, Namespace

from services.equity_service import EquityService

app_api = Blueprint('app_api', __name__)

@app_api.route('/client', methods=['GET'])
def health():
    return render_template('index.html')

@app_api.route('/<path:filename>', methods=['GET'])
def get_file(filename):
    directory = 'static/dist'  # Path to your static files

    # Determine MIME type based on file extension
    if filename.endswith('.css'):
        mimetype = 'text/css'
    elif filename.endswith('.js'):
        mimetype = 'application/javascript'
    else:
        mimetype = None
    return send_from_directory(directory, filename, mimetype=mimetype)