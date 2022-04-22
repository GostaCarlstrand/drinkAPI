from app import db
from controllers.api_controller import generate_api_key, get_drinks_by_name
from models import User, Drinks


def get_all_users():
    return User.query.filter(User.id).all()


def get_user_by_id(user_id):
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
    return Drinks.query.filter_by(user_id=user.id).first()


def access_drink(user, drink_name):
    """
    Check if user has access to modify the drink
    :return:
    """
    # Get all drinks with that name
    drinks = get_drinks_by_name(drink_name)

    for drink in drinks:
        if user.id == drink.user_id:
            return True
    return False


def access_to_modify(api_key, drink_name):
    """
    If the user has access to modify the drink
    :param (api_key, drink_name)
    :return: True
    """
    user = get_user_by_key(api_key)
    if access_drink(user, drink_name):
        return True
    else:
        return False


def insert_user(user_data):
    api_key = generate_api_key()
    new_user = User(name=user_data['name'], admin=user_data['admin'], api_key=api_key)
    db.session.add(new_user)
    db.session.commit()
    return api_key




