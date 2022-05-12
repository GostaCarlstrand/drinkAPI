"""
Unit tests for POST end-point
"""
import pytest
from app import create_app



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
    headers_dict = {"api_key": "I3WBR11CQ6NFZDI"}
    response = client.post("/api/v1/drink/", headers=headers_dict)
    assert response.status_code == 200
