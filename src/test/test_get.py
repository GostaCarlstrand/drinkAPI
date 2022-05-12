"""
Unit tests for GET end-point
"""
from app import create_app
import pytest



@pytest.fixture
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


def test_get(client):
    """
    Test the api HTTP status code
    :param client: An app test client.
    :return: OK
    """
    response = client.get("/admin/drink")
    assert response.status_code == 404


def test_get_first(client):
    """
    Test the api HTTP status code
    :param client: An app test client
    :return: OK
    """
    response = client.get("/signup")
    assert response.status_code == 200

def test_get_second(client):
    """
    Test the api HTTP status code
    :param client: An app test client
    :return: 401 error due to invalid api-key
    """
    response = client.get("/api/v1/drink/<alcohol>")
    assert response.status_code == 401

def test_get_third(client):
    """
    Test the api HTTP status code
    :param client: An app test client
    :return: Get all drinks. OK
    """
    x = {"api_key": "I3WBR11CQ6NFZDI"}
    response = client.get("/api/v1/drink/", headers=x)
    assert response.status_code == 200

def test_get_fourth(client):
    """
    Test the api HTTP status code
    :param client: An app test client
    :return: Data on drinks. OK
    """
    x = {"api_key": "I3WBR11CQ6NFZDI"}
    response = client.get("/api/v1/drink/<alcohol>", headers=x)
    assert response.status_code == 200




