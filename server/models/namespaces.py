from flask_restx import Namespace

def eq_ns_namespace():
    return Namespace('equity', description='Equity operations', path='/api/v1/equity')

