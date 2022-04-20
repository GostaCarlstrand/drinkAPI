import string
import random


def insert_user(user_data):
    api_key = generate_api_key()
    """
    MISSING DB
    Save the key, user data and admin in database
    """

    user = {
        'user_data': user_data['name'],
        'admin': user_data['admin'],
        'api_key': api_key
    }

    with open('api_users.txt', 'a', encoding='utf-8') as file:
        file.write(f"{str(user)}\n")
    return api_key


def generate_api_key():
    key_length = 15
    # Creates a string that contains random characters from the alphabet and digits 0-9
    api_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=key_length))

    return api_key


def confirm_api_key(user_key):
    """
    MISSING DB
    Needs to extract a list of users from db and compare the keys with the user_key provided from the api request
    """
    with open('api_users.txt', 'r', encoding='utf-8') as users:
        for user in users:
            if user_key in user:
                return True
        return False


