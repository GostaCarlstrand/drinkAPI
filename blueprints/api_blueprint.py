"""
Integration of the API
"""
import json
from functools import wraps
from flask import Blueprint, request, Response, jsonify
from controllers.api_controller import api_usage, confirm_api_key, get_drinks_by_alcohol, \
    get_all_drinks, create_drink, modify_user_drink, remove_none, delete_one_drink
from controllers.user_controller import access_to_modify

api_blueprint = Blueprint('api_blueprint', __name__)


def authorize_api_key(func):
    """
    A decorator to check that the request has a valid API-key
    :param f:
    :return: wrapper function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extracted from the params in the api request
        key = request.headers.get('api_key')

        if not confirm_api_key(key):
            response = {
                'Result': "Your API key is invalid"
            }
            return Response(json.dumps(response), 401, content_type='application/json')
        return func(*args, **kwargs)

    return wrapper


def authorize_modify_db(func):
    """
    A decorator to check that the user has access to modify the drink
    :param f:
    :return: wrapper function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extracted from the params in the api request
        if 'drink_id' not in request.json:
            return Response("'Status':'Error, drink id is missing'",
                            400, content_type='application/json')
        key = request.headers.get('api_key')
        drink_id = request.json['drink_id']
        if not isinstance(drink_id, int):
            response = {
                'Status': "Error, drink_id must be a number"
            }
            return Response(json.dumps(response), 400, content_type='application/json')
        # Can be changed depending on what the request looks like
        if not access_to_modify(key, drink_id):
            response = {
                'Result': "No drink to modify"
            }
            return Response(json.dumps(response), 401, content_type='application/json')
        return func(*args, **kwargs)

    return wrapper


@api_blueprint.before_request
@authorize_api_key
def before_request():
    """
    Function that is called before an api request
    """
    endpoint = request.base_url
    api_key = request.headers.get('api_key')
    api_usage(api_key, endpoint)


def hateoas_links():
    """
    Returns links that are used in the response to the user
    :return: Dict with links
    """
    links = [
        {
            'description': "Endpoint can be used for deleting,"
                           " creating, reading and modifying drinks",
            'href': 'self',
            'rel': '/drink',
            'type': ["GET", "PUT", "POST", "DELETE"]
        },
        {
            'description': "Get data on drinks with an given component",
            'href': '/drink/component_name',
            'rel': 'component name',
            'type': ["GET"]
        }
    ]

    return links


@api_blueprint.delete('/api/v1/drink/')
@authorize_modify_db
def delete_drink():
    """
    Delete the drink with the given drink id
    :return: A response that includes data about the drink that has been deleted
    """
    data = request.json
    drink_id = data['drink_id']
    deleted_drink = delete_one_drink(drink_id).__dict__
    deleted_drink.pop("_sa_instance_state")
    response = jsonify({'data': deleted_drink, 'links': hateoas_links()})
    return response


@api_blueprint.put('/api/v1/drink/')
@authorize_modify_db
def modify_drink():
    """
    Allows the user to modify any drink that the user has contributed
    :return: Response with status code
    """
    data = request.json
    modify_user_drink(data)
    response = jsonify({'Status': 'Modification succeeded', 'links': hateoas_links()})
    return response


@api_blueprint.post('/api/v1/drink/')
def post_new_drink():
    """
    Allows the user the add a new drink to the db
    :return: Response with status code
    """
    data = request.json
    api_key = request.headers.get('api_key')
    if 'ingredients' in data and 'name' in data:
        create_drink(data, api_key)
        response = jsonify({'Status': 'Added drink to database', 'links': hateoas_links()})
        return response
    response = jsonify({'Status': 'Error, ingredients or name is missing',
                        'links': hateoas_links()})
    return response


@api_blueprint.get('/api/v1/drink/')
def get_all_drink():
    """
    To get all drinks in the db
    :return: List with drinks
    """
    list_drinks = []
    all_drinks = get_all_drinks()
    for drink in all_drinks:
        drink.__dict__.pop('_sa_instance_state')
        list_drinks.append(drink.__dict__)

    list_drinks = remove_none(list_drinks)
    response = jsonify({'Drinks': list_drinks, 'links': hateoas_links()})
    return response


@api_blueprint.get('/api/v1/drink/<alcohol>')
def get_alcohol(alcohol):
    """
    Get data on drinks with given name
    :param alcohol:
    :return: List with drinks
    """
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
        alco_data['ingredients'] = \
            [alco.strIngredient1, alco.strIngredient2,
             alco.strIngredient3, alco.strIngredient4,
             alco.strIngredient5, alco.strIngredient6,
             alco.strIngredient7, alco.strIngredient8,
             alco.strIngredient9, alco.strIngredient10,
             alco.strIngredient11, alco.strIngredient12]
        output.append(alco_data)

    clean_list = remove_none(output)
    response = jsonify({'Drinks': clean_list, 'links': hateoas_links()})
    return response
