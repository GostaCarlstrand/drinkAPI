from flask import flash, redirect, url_for, render_template

from app import db
from controllers.api_controller import generate_api_key, get_drinks_by_name, get_drink_by_id
from models import User, Drinks
from sqlalchemy import and_, or_, not_


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




