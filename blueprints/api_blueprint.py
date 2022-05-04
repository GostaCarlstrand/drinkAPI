import json
from functools import wraps
from flask import Blueprint, request, Response, jsonify
from controllers.api_controller import api_usage, delete_drinks, confirm_api_key, get_drinks_by_alcohol, get_all_drinks
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
        key = request.headers.get('api_key')

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
        data = request.json
        key = request.headers.get('api_key')
        drink_name = data['test']
        # Can be changed depending on what the request looks like
        if not access_to_modify(key, drink_name):
            response = {
                'Result': "No drink to modify"
            }
            return Response(json.dumps(response), 401, content_type='application/json')
        return f(*args, **kwargs)

    return wrapper


@api_blueprint.before_request
@authorize_api_key
def before_request():
    endpoint = request.base_url
    api_key = request.headers.get('api_key')
    api_usage(api_key, endpoint)


@api_blueprint.delete('/api/v1/drink/')
@authorize_modify_db
def delete_all_drinks():
    """
    Deletes drinks from the user, only drinks with the same name are affected
    :return:
    """
    data = request.json
    # Drink that is passed in the query string
    api_key = request.headers.get('api_key')
    drink_name = data['test']
    delete_drinks(api_key, drink_name)
    return Response("'Status':'Deletion succeeded'", 200, content_type='application/json')


@api_blueprint.get('/api/v1/drink/')
def get_all_drink():
    all_drinks = get_all_drinks()
    return jsonify({'Drinks': all_drinks})


@api_blueprint.get('/api/v1/drink/<alcohol>')
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

