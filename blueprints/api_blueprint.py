import json
from functools import wraps
from flask import Blueprint, request, Response, jsonify
from controllers.api_controller import api_usage, delete_drinks, confirm_api_key, get_drinks_by_alcohol
from controllers.user_controller import access_to_modify
from models import Drinks

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
        key = request.headers.get('api_key')
        print()
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
        drink_name = data['drink']
        # Can be changed depending on what the request looks like
        if not access_to_modify(key, drink_name):
            response = {
                'Result': "No drink to modify"
            }
            return Response(json.dumps(response), 401, content_type='application/json')
        return f(*args, **kwargs)

    return wrapper


def data_usage(f):
    """
    A decorator that should be set for all api requests. Store details about the request in the database
    :param f:
    :return: wrapper function
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        endpoint = request.base_url
        data = request.args
        api_key = data['api_key']
        api_usage(api_key, endpoint)
        return f(*args, **kwargs)

    return wrapper


@api_blueprint.delete('/api/v1/drink/')
@authorize_api_key
@authorize_modify_db
@data_usage
def delete_all_drinks():
    """
    Deletes drinks from the user, only drinks with the same name are effected
    :return:
    """
    data = request.args
    # Drink that is passed in the query string
    api_key = data['api_key']
    drink_name = data['drink']
    delete_drinks(api_key, drink_name)
    return Response("'Status':'Deletion succeeded'", 200, content_type='application/json')


@api_blueprint.get('/api/v1/drink/')
@authorize_api_key
@authorize_modify_db
@data_usage
def get_recipe_drink():
    # Temp fake data that is return
    data = request.args

    drink_recipe = {
        'main': 'vodka',
        'sub': 'gin',
    }
    return Response(json.dumps(drink_recipe), 200, content_type='application/json')


@api_blueprint.get('/api/v1/drink/<alcohol>')
@authorize_api_key
def get_alcohol(alcohol):
    alcohol = get_drinks_by_alcohol(alcohol)

    output = []
    for alco in alcohol:
        alco_data = {}
        alco_data['name'] = alco.strDrink
        alco_data['alcohol'] = alco.strAlcoholic
        alco_data['category'] = alco.strCategory
        alco_data['glass'] = alco.strGlass
        alco_data['instructions'] = alco.strInstructions
        alco_data['ingredients'] = [alco.strIngredient1, alco.strIngredient2, alco.strIngredient3, alco.strIngredient4,
                                    alco.strIngredient5, alco.strIngredient6, alco.strIngredient7, alco.strIngredient8,
                                    alco.strIngredient9, alco.strIngredient10, alco.strIngredient11,
                                    alco.strIngredient12]
        output.append(alco_data)

    clean_list = remove_none(output)

    return jsonify({'Drinks': clean_list})


def remove_none(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)((remove_none(k), remove_none(v))
                         for k, v in obj.items() if k is not None and v is not None)
    else:
        return obj

