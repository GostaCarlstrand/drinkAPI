"""
Create POST endpoint, add new drinks to the database
"""
from app import create_app
import pytest

@pytest.fixture
def client():
    app = create_app()
    # Testläge
    app.config['TESTING'] = True

    # Test client
    with app.app_context():
        with app.test_client() as api_client:
            yield api_client

# Nedan kommer köra ovan(client). Yield är samma som return men istället för att stanna, kör den om o om igen.
def test_post(client):
    response = client.get("/user")
    assert response.status_code == 200
