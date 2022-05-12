"""
Unit tests for data
"""


import pytest
from app import create_app



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
    headers_dict = {"api_key": "I3WBR11CQ6NFZDI"}
    headers_api = client.get('/api/v1/drink/1', headers=headers_dict)
    assert headers_api.json == {'Drinks': [{'alcohol': 'Alcoholic','category': 'Shot',
    'glass': 'Old-fashioned glass','id': 1,'ingredients':['Absolut Kurant',
    'Grand Marnier','Chambord raspberry liqueur',
    'Midori melon liqueur','Malibu rum','Amaretto','Cranberry juice','Pineapple juice'],
    'instructions':'Shake ingredients in a mixing tin filled with ice cubes. Strain into a glass.',
    'name': '1-900-FUK-MEUP'}],}

def test_data_alcohol(client):
    """
    Test the data from a call /<alcohol>
    :param client: An app test client
    :return: Data on drinks with alcohol
    """
    headers_dict = {"api_key": "I3WBR11CQ6NFZDI"}
    headers_api = client.get('/api/v1/drink/<alcohol>', headers=headers_dict)
    assert headers_api.json == {'Drinks': []}
