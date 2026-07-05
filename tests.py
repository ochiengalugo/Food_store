import pytest
from app import app, inventory_db

@pytest.fixture
def client():
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_all_items(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_single_item(client):
    
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.get_json()['product_name'] == "Nutella 400g"

    
    response = client.get('/inventory/999')
    assert response.status_code == 404
