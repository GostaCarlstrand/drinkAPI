"""
Unit tests for POST end-point
"""
import json
from unittest.mock import patch, Mock
from nose.tools import assert_list_equal
import pytest
import requests
from flask import request

from app import create_app
from controllers.user_controller import insert_user


@pytest.fixture
def client():
    """
    Test fixture for api client
    :return: yields a test client
    """
    app = create_app()
    app.config['TESTING'] = True


    with app.app_context():
        with app.test_client() as api_client:
            yield api_client


def test_post(client):
    """
    Test the data from a call to the POST end-point
    :param client: An app test client from the fixture
    :return: None
    """
    x = {"api_key": "I3WBR11CQ6NFZDI"}
    response = client.post("/api/v1/drink/", headers=x)
    assert response.status_code == 200

@patch('blueprints.open_blueprint.sign_up.post')
def test_data_post(client):
    data = {
        'name': 'Dan',
        'admin': True,
        'api_key': "I3WBR11CQ6NFZDI"
    }
    client.return_value = Mock(ok=True)
    client.return_value.json.return_value = data

    response = get_todos
    assert_list_equal(response.json,data)
    #x = {"api_key": "I3WBR11CQ6NFZDI"}
    #api_key = insert_user({'name': 'Max', 'admin': True})
    #response = client.post("/signup")
    #assert response.status_code == 200

