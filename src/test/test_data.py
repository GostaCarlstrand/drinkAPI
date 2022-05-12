"""
Unit tests for data
"""
import dataclasses
import json
from os import name
from typing import Any
from unittest import mock

import pytest, pytest_flask
from sqlalchemy.testing import db

import app
from app import create_app, admin
from controllers.user_controller import get_user_by_key

from models import Drinks, User


@pytest.fixture(scope='module')
def client():
    """
    Test fixture for api client
    :return: yields a test client
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_test.sqlite'
    with app.app_context():
        with app.test_client() as api_client:
            yield api_client


def test_data_one(client):
    """
    Test the data from a call /1
    :param client: An app test client
    :return: Data on a drink
    """
    x = {"api_key": "I3WBR11CQ6NFZDI"}
    rv = client.get('/api/v1/drink/1', headers=x)
    assert rv.json == {'Drinks': [{'alcohol': 'Alcoholic','category': 'Shot','glass': 'Old-fashioned glass','id': 1,'ingredients': ['Absolut Kurant','Grand Marnier','Chambord raspberry liqueur','Midori melon liqueur','Malibu rum','Amaretto','Cranberry juice','Pineapple juice'],'instructions': 'Shake ingredients in a mixing tin filled with ice cubes. Strain into a rocks glass.','name': '1-900-FUK-MEUP'}],}

def test_data_alcohol(client):
    """
    Test the data from a call /<alcohol>
    :param client: An app test client
    :return: Data on drinks with alcohol
    """
    x = {"api_key": "I3WBR11CQ6NFZDI"}
    rv = client.get('/api/v1/drink/<alcohol>', headers=x)
    assert rv.json == {'Drinks': []}

def test_get_drink_name( client):

    api_key = "I3WBR11CQ6NFZDI"
    data = 'sqlite:///db_test.sqlite'
    drink = Drinks
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


















