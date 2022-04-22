from datetime import datetime

from app import db
from models import User, Drinks, DataUsage


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


def access_to_modify(api_key):
    """
    Function that return a boolean if there is a drink in the database that the user has created
    :param api_key
    :return: True
    """
    user = get_user_by_key(api_key)
    drink = get_user_drinks(user)
    if drink:
        return True
    else:
        return False




