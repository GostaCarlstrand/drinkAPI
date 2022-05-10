"""
Unit tests for PUT end-point
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


    with app.app_context():
        with app.test_client() as api_client:
            yield api_client


def test_put(client):
    """
        Test the data from a call to the PUT end-point
        :param client: An app test client from the fixture
        :return: None
        """
    response = client.put("/admin/drinks/")
    assert response.status_code == 200
