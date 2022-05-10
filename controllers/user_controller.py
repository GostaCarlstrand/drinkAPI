"""
Data on users
"""
import json
from flask import Response
from app import db
from controllers.api_controller import generate_api_key, get_drink_by_id
from models import User, Drinks, DataUsage


def get_all_users():
    """
    Get all users from db
    :return: List with User objects
    """
    return User.query.filter(User.id).all()


def get_user_by_id(user_id):
    """
    Get a user by their id
    :param user_id:
    :return: User object
    """
    return User.query.filter(User.id == user_id).first()


def get_user_by_key(api_key):
    """
    A function that finds the user to which the provided api key belongs to
    :param api_key:
    :return: User object from database
    """
    return User.query.filter_by(api_key=api_key).first()


def get_user_drinks(user):
    """
    Function to get all drinks that belong to a specific user
    :return: If any, drinks as objects
    """
    return Drinks.query.filter_by(user_id=user.id).all()


def get_user_requests(user):
    """
    Function to get last total request amount that belong to a specific user
    :return: last object in DataUsage for specific user
    """
    return DataUsage.query.filter_by(user_id=user.id).order_by(DataUsage.id.desc()).first()


def access_to_modify(api_key, drink_id):
    """
    If the user has access to modify the drink
    :param (api_key, drink_name)
    :return: True
    """
    user = get_user_by_key(api_key)
    drink = get_drink_by_id(drink_id)

    if drink and user.id == drink.user_id:
        return True
    return False


def insert_user(user_data):
    """
    Insert a new user into the db
    :param user_data:
    :return: User api key
    """

    api_key = generate_api_key()
    new_user = User(name=user_data['name'], admin=user_data['admin'], api_key=api_key)
    db.session.add(new_user)
    db.session.commit()
    return api_key


def check_user_keys(user_info):
    """
    Check that the keys in the user update is correct
    :param json_response: user input for update
    :return: None if no errors, a Response object if an error is found
    """
    accepted_keys = ['name', 'admin', 'api_key']

    for key in user_info:
        if key not in accepted_keys:
            return Response(json.dumps({'Error': f'The key '
                                                 f'{key} is not accepted in the json request'}),
                            400, content_type='application/json')

    for key in accepted_keys:
        if key not in user_info:
            return Response(json.dumps({'Error': f'The required key '
                                                 f'{key} is not present in the json request'}),
                            400, content_type='application/json')
    return None


def user_check(user_id):
    """
    Check if user_id is an integer
    :param user_id: user input
    :return: user_id if no errors
    """
    if user_id.isdigit():
        user_id = int(user_id)
    else:
        return Response(json.dumps({'Error': 'Id must be an integer'}),
                        400, content_type='application/json')

    user_id = get_user_by_id(user_id)

    if not user_id:
        return Response(json.dumps({'Error': 'User is not present in the database'}),
                        404, content_type='application/json')
    return user_id
