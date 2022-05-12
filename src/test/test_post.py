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


