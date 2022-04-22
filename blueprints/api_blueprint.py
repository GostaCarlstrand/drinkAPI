import json
from functools import wraps
from flask import Blueprint, render_template, request, Response

from controllers.dev_controller import confirm_api_key
from controllers.user_controller import access_to_modify

api_blueprint = Blueprint('api_blueprint', __name__)



def authorize_api_key(f):
    """
    A decorator to check that the request has a valid API-key
    :param f:
    :return: wrapper function
    """
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


def authorize_modify_db(f):
    """
    A decorator to check that the user has access to modify the drink
    :param f:
    :return: wrapper function
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        # Extracted from the params in the api request
        data = request.args
        key = data['api_key']
        # Can be changed depending on what the request looks like
        if not access_to_modify(key):
            response = {
                'Result': "No drink to modify"
            }
            return Response(json.dumps(response), 401, content_type='application/json')
        return f(*args, **kwargs)

    return wrapper


@api_blueprint.post('/api/v1/drink/modify')
@authorize_modify_db
def delete_drink():
    data = request.args
    # Drink that is passed in the query string
    drink_name = data['drink']

    return Response("'Status':'You have deleted'", 200, content_type='application/json')


@api_blueprint.get('/api/v1/drink/')
@authorize_api_key
def get_recipe_drink():
    # Temp fake data that is return
    data = request.args



    drink_recipe = {
        'main': 'vodka',
        'sub': 'gin',
    }
    return Response(json.dumps(drink_recipe), 200, content_type='application/json')

