import json
from functools import wraps
from flask import Blueprint, request, Response, jsonify
from controllers.api_controller import api_usage, delete_drinks, confirm_api_key, get_drinks_by_alcohol, get_all_drinks, \
    create_drink, modify_user_drink
from controllers.user_controller import access_to_modify

api_blueprint = Blueprint('api_blueprint', __name__)


"""
name - name of drink
alcohol - if alcohol or not
category - Label for what type of drink, cocktail for example
glass - If user recommends specific type of glass
instructions - Instructions on how to make the drink
ingredients - A list with the ingredients needed to make the drink
"""


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
        if 'drink_id' in data:
            if not isinstance(data['drink_id'], int):
                response = {
                    'Status': "Error, drink_id must be a number"
                }
                return Response(json.dumps(response), 400, content_type='application/json')
        drink_id = data['drink_id']
        # Can be changed depending on what the request looks like
        if not access_to_modify(key, drink_id):
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
# Do not work atm @authorize_modify_db
def delete_all_drinks():
    """
    Deletes drinks from the user, only drinks with the same name are affected
    :return:
    """
    data = request.json
    # Drink that is passed in the query string
    api_key = request.headers.get('api_key')
    drink_name = data['name']
    delete_drinks(api_key, drink_name)
    return Response("'Status':'Deletion succeeded'", 200, content_type='application/json')


@api_blueprint.put('/api/v1/drink/')
@authorize_modify_db
def modify_drink():
    data = request.json
    if 'drink_id' in data:
        modify_user_drink(data)
        return Response("'Status':'Modification succeeded'", 200, content_type='application/json')
    else:
        return Response("'Status':'Error, drink id is missing'", 400, content_type='application/json')


@api_blueprint.post('/api/v1/drink/')
def post_new_drink():
    data = request.json
    api_key = request.headers.get('api_key')
    if 'ingredients' in data and 'name' in data:
        create_drink(data, api_key)
        return Response("'Status':'Added drink to database'", 200, content_type='application/json')
    else:
        return Response("'Status':'Error, ingredients or name is missing'", 400, content_type='application/json')


@api_blueprint.get('/api/v1/drink/')
def get_all_drink():
    list_drinks = []
    all_drinks = get_all_drinks()
    for drink in all_drinks:
        drink.__dict__.pop('_sa_instance_state')
        list_drinks.append(drink.__dict__)

    return jsonify({'Drinks': list_drinks})


@api_blueprint.get('/api/v1/drink/<alcohol>')
def get_alcohol(alcohol):
    alcohol = get_drinks_by_alcohol(alcohol)

    output = []
    for alco in alcohol:
        alco_data = {}
        alco_data['id'] = alco.index
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

