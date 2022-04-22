from datetime import datetime
import string
import random
from app import db
from models import Drinks, DataUsage, User


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


def delete_a_drink(drink_name):
    drink = get_drinks_by_name(drink_name)


def generate_api_key():
    key_length = 15
    # Creates a string that contains random characters from the alphabet and digits 0-9
    api_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=key_length))
    return api_key


def confirm_api_key(api_key):
    if User.query.filter_by(api_key=api_key).first():
        return True
    else:
        return False
