import json
from functools import wraps
from flask import Blueprint, render_template, request, Response

from mongo_handler import confirm_api_key

api_blueprint = Blueprint('api_blueprint', __name__)


# Add this as a decorator to check that the request has a valid API-key
def authorize_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Extracted from the params in the api request
        key = request.args.get('api_key')
        if not confirm_api_key(key):
            response = {
                'Result': "Your API key is invalid"
            }
            return Response(json.dumps(response), 401, content_type='application/json')
        return f(*args, **kwargs)
    return wrapper


@api_blueprint.get('/api/v1/drink/')
@authorize_api_key
def get_recipe_drink():
    # Temp fake data that is return
    drink_recipe = {
        'main': 'vodka',
        'sub': 'gin',
    }
    return Response(json.dumps(drink_recipe), 200, content_type='application/json')

