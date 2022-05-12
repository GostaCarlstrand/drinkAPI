"""
Unit tests for DELETE end-point
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


def test_delete(client):
    """
    Test the data from a call to the DELETE end-point
    :param client: An app test client from the fixture
    :return: None
    """
    x = {"api_key": "I3WBR11CQ6NFZDI"}
    response = client.delete("/api/v1/drink/", headers=x)
    assert response.status_code == 200