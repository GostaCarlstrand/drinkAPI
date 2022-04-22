from models import Drinks


def get_all_drinks():
    """
    Function to get all drinks from the database
    :return: Drinks as objects
    """
    return Drinks.query.all()
