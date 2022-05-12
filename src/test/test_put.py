"""
Unit tests for PUT end-point
"""
import pytest
from flask import request
from app import create_app
from controllers.api_controller import modify_user_drink


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


def test_put(client):
    """
    Test the data from a call to the PUT end-point
    :param client: An app test client from the fixture
    :return: None
    """
    headers_dict = {"api_key": "Y5YO2YDQZV2AZPW"}
    response = client.put("/api/v1/user/<user_id>", headers=headers_dict)
    assert response.status_code == 200
