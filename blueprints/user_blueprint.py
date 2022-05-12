"""
Blueprint that contains endpoints related to user data
"""

from flask import Blueprint, jsonify, request
from app import db
from blueprints.api_blueprint import authorize_api_key
from controllers.api_controller import api_usage
from controllers.user_controller import get_all_users, get_user_by_key, \
    user_check, check_user_keys, get_user_drinks, get_user_by_id

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.before_request
@authorize_api_key
def before_request():
    """
    Function that is called before every request
    :return: No return value
    """
    endpoint = request.base_url
    api_key = request.headers.get('api_key')
    api_usage(api_key, endpoint)


@user_blueprint.get('/api/v1/users/')
def get_users():
    """
    Get all API users
    :return: List of users
    """
    list_users = []
    all_users = get_all_users()
    for user in all_users:
        user.__dict__.pop('_sa_instance_state')
        list_users.append(user.__dict__)

    links = [
        {
            'description': 'Get all users',
            'href': 'self',
            'rel': 'users',
            'type': ["GET"]
        },
        {
            'description': 'Get or modify user data',
            'href': 'users/user_id',
            'rel': 'user_id',
            'type': ["GET", "PUT"]
        },
        {
            'description': 'Get user drinks',
            'href': 'users/user_id/drinks',
            'rel': 'drinks',
            'type': ["GET"]
        }
    ]

    return jsonify({'Users': list_users, 'links': links})


@user_blueprint.get('/api/v1/users/<user_id>')
def profile_get_user(user_id):
    """
    Get a user by id
    :param user_id:
    :return: One user
    """
    user = user_check(user_id)
    user = user.__dict__
    links = [
        {
            'description': 'Get or modify user data',
            'href': 'users/user_id',
            'rel': 'user_id',
            'type': ["GET", "PUT"]
        },
        {
            'description': 'Get user drinks',
            'href': 'users/user_id/drinks',
            'rel': 'drinks',
            'type': ["GET"]
        }
    ]

    user.pop('_sa_instance_state')
    return jsonify({'user': user, 'links': links})


@user_blueprint.get('/api/v1/users/<user_id>/drinks')
def profile_get_user_drinks(user_id):
    """
    Get all drinks that was created by the user with the given user id
    :param user_id:
    :return:
    """
    list_drinks = []
    drinks = get_user_drinks(get_user_by_id(int(user_id)))
    for drink in drinks:
        drink.__dict__.pop('_sa_instance_state')
        list_drinks.append(drink.__dict__)

    links = [
        {
            'description': 'Get user drinks',
            'href': 'users/user_id/drinks',
            'rel': 'drinks',
            'type': ["GET"]
        }
    ]

    return jsonify({'drinks': list_drinks, 'links': links})


@user_blueprint.put('/api/v1/users/<user_id>')
def update_user(user_id):
    """
    Change details about a user
    :param user_id:
    :return: A response with a status message
    """
    user = user_check(user_id)
    api_key = request.headers.get('api_key')
    user_key = get_user_by_key(api_key)

    update_user_info = request.json
    response = check_user_keys(update_user_info)
    if response:
        return response

    if user == user_key:
        user.name = update_user_info['name']
        user.admin = update_user_info['admin']
        user.api_key = update_user_info['api_key']
        db.session.commit()

    links = [
        {
            'description': 'Get or modify user data',
            'href': 'users/user_id',
            'rel': 'user_id',
            'type': ["GET", "PUT"]
        },
        {
            'description': 'Get user drinks',
            'href': 'users/user_id/drinks',
            'rel': 'drinks',
            'type': ["GET"]
        }
    ]
    return jsonify({'Status': 'User updated', 'links': links})
