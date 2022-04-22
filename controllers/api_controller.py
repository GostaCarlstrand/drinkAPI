from datetime import datetime

from app import db
from controllers.user_controller import get_user_by_key
from models import Drinks, DataUsage


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
    return Drinks.query.filter_by(strDrink=drink_name).all()


def api_usage(api_key, endpoint):
    """
    Stores the amount of api calls that the user has made
    :param (api_key, endpoint)
    :return:
    """
    user = get_user_by_key(api_key)
    date = datetime.now()
    # Data amount should be calculated somehow
    db.session.add(DataUsage(endpoint=endpoint, user_id=user.id, timestamp=date, data_amount=10))
    db.session.commit()
    return


def delete_a_drink(drink_name):
    drink = get_drinks_by_name(drink_name)


