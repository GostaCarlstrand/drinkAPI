"""
Data on all drinks
"""
from datetime import datetime
import string
import random
from sqlalchemy import or_
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


def get_drinks_by_alcohol(alcohol_data):
    """
    Get drinks from db with or without alcohol
    :param alcohol_data:
    :return: List with alcohol or nonalcoholic drinks
    """


    query =  Drinks.query.filter(
        or_(
            Drinks.index.like(alcohol_data),
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
    """
    from controllers.user_controller import get_user_requests, get_user_by_key
    user = get_user_by_key(api_key)
    date = datetime.now()
    # Data amount should be calculated somehow
    total_requests = get_user_requests(user)

    if total_requests is None:
        total_requests = 1
    else:
        total_requests = total_requests.total_requests + 1

    db.session.add(DataUsage(endpoint=endpoint, user_id=user.id,
                             timestamp=date, total_requests=total_requests))
    db.session.commit()



def delete_drinks(api_key, drink_name):
    """
    Deletes all drinks with the given name. Only affects the authorized users drinks
    :param api_key:
    :param drink_name:
    :return:
    """
    from controllers.user_controller import get_user_drinks, get_user_by_key
    user = get_user_by_key(api_key)
    drinks = get_user_drinks(user)
    for drink in drinks:
        if drink.strDrink == drink_name:
            db.session.delete(drink)
    db.session.commit()


def delete_one_drink(drink_id):
    """
    Deletes the drink with the given drink_id
    :param drink_id:
    :return: The drink that has been deleted from the db
    """
    temp = Drinks.query.filter_by(index=drink_id).first()
    db.session.delete(Drinks.query.filter_by(index=drink_id).first())
    db.session.commit()
    return temp


def generate_api_key():
    """
    Generates a string with random characters
    :return: User API key
    """
    key_length = 15
    # Creates a string that contains random characters from the alphabet and digits 0-9
    api_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=key_length))
    return api_key


def confirm_api_key(api_key):
    """
    Checks if the api key is in db
    :param api_key:
    :return: Boolean value
    """
    return User.query.filter(User.api_key == api_key).first()


def create_drink(data, api_key):
    """
    Uses user input to store a drink in the db
    :param data:
    :param api_key:
    """
    from controllers.user_controller import get_user_by_key
    drink = Drinks()
    if 'alcohol' in data:
        drink.strAlcoholic = data['alcohol']
    if 'category' in data:
        drink.strCategory = data['category']
    if 'glass' in data:
        drink.strGlass = data['glass']
    if 'instructions' in data:
        drink.strInstructions = data['instructions']

    drink.assign_ingredients(data['ingredients'])

    user = get_user_by_key(api_key)
    drink.user_id = user.id
    drink.strDrink = data['name']
    db.session.add(drink)
    db.session.commit()


def get_drink_by_id(drink_id):
    """
    Get a drink using the drink id
    :param drink_id:
    :return: Drink
    """
    return Drinks.query.filter_by(index=drink_id).first()


def modify_user_drink(data):
    """
    Updates information about the drink
    :param data:
    """
    drink_cursor = db.session.query(Drinks).filter(Drinks.index == data['drink_id'])

    def update(new_data):
        drink_cursor.update(new_data, synchronize_session="fetch")

    drink = get_drink_by_id(data['drink_id'])

    if 'name' in data:
        if not data['name'] == drink.strDrink:
            update({'strDrink': data['name']})
    if 'alcohol' in data:
        if not data['alcohol'] == drink.strAlcoholic:
            update({'strAlcoholic': data['alcohol']})
    if 'category' in data:
        if not data['category'] == drink.strCategory:
            update({'strCategory': data['category']})
    if 'glass' in data:
        if not data['glass'] == drink.strGlass:
            update({'strGlass': data['glass']})
    if 'instructions' in data:
        if not data['instructions'] == drink.strInstructions:
            update({'strInstructions': data['instructions']})

    for count, ingredient in enumerate(data['ingredients']):
        count += 1
        str_builder = "strIngredient"
        str_builder += str(count)
        if ingredient != drink.strIngredient1 and count == 1:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient2 and count == 2:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient3 and count == 3:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient4 and count == 4:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient5 and count == 5:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient6 and count == 6:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient7 and count == 7:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient8 and count == 8:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient9 and count == 9:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient10 and count == 10:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient11 and count == 11:
            update({str_builder: ingredient})
            continue
        if ingredient != drink.strIngredient12 and count == 12:
            update({str_builder: ingredient})
            continue
    db.session.commit()


def remove_none(obj):
    """
    Removes all None values
    :param obj:
    :return: Drink object
    """
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    if isinstance(obj, dict):
        return type(obj)((remove_none(k), remove_none(v))
                         for k, v in obj.items() if k is not None and v is not None)
    return obj
