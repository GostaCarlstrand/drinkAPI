from datetime import datetime
import string
import random
from app import db
from models import Drinks, DataUsage, User
from sqlalchemy import and_, or_, not_


def get_all_drinks():
    """
    Function to get all drinks from the database
    :return: Drinks as objects
    """
    return Drinks.query.all()


def get_drinks_by_name(drink_name):
    """
    Get drinks from db with a specific name
    :param drink_name:
    :return: List with drinks
    """

    data = Drinks.query.filter_by(strDrink=drink_name).all()
    return data


def get_drinks_by_alcohol(alcohol_data):
    """
    Get drinks from db with or without alcohol
    :param alcohol_data:
    :return: List with alcohol or nonalcoholic drinks
    """

    query = Drinks.query.filter(
        or_(
            Drinks.strDrink.like(alcohol_data),
            Drinks.strAlcoholic.like(alcohol_data),
            Drinks.strIngredient1.like(alcohol_data),
            Drinks.strIngredient2.like(alcohol_data),
            Drinks.strIngredient3.like(alcohol_data),
            Drinks.strIngredient4.like(alcohol_data),
            Drinks.strIngredient5.like(alcohol_data),
            Drinks.strIngredient6.like(alcohol_data),
        )
    )
    return query


def api_usage(api_key, endpoint):
    """
    Stores the amount of api calls that the user has made
    :param (api_key, endpoint)
    :return:
    """
    from controllers.user_controller import get_user_by_key
    user = get_user_by_key(api_key)
    date = datetime.now()
    # Data amount should be calculated somehow
    db.session.add(DataUsage(endpoint=endpoint, user_id=user.id, timestamp=date, data_amount=10))
    db.session.commit()
    return


def delete_drinks(api_key, drink_name):
    """
    Deletes all drinks with the given name. Only affects the authorized users drinks
    :param api_key:
    :param drink_name:
    :return:
    """
    from controllers.user_controller import get_user_by_key
    from controllers.user_controller import get_user_drinks
    user = get_user_by_key(api_key)
    drinks = get_user_drinks(user)
    [db.session.delete(drink) for drink in drinks if drink.strDrink == drink_name]
    db.session.commit()
    return


def generate_api_key():
    key_length = 15
    # Creates a string that contains random characters from the alphabet and digits 0-9
    api_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=key_length))
    return api_key


def confirm_api_key(api_key):
    if User.query.filter(User.api_key == api_key).first():
        return True
    else:
        return False
