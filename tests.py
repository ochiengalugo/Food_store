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

# 2. Test GET /inventory/<id> (Fetch single item)
def test_get_single_item(client):
    # Test valid item
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.get_json()['product_name'] == "Nutella 400g"

    # Test invalid item
    response = client.get('/inventory/999')
    assert response.status_code == 404

# 3. Test POST /inventory (Add item)
def test_add_item(client):
    new_item = {
        "product_name": "Test Apple",
        "code": "1111111111111",
        "brands": "Fruit Co",
        "price": 0.99,
        "quantity": 10
    }
    response = client.post('/inventory', json=new_item)
    assert response.status_code == 201
    assert response.get_json()['product_name'] == "Test Apple"
    assert response.get_json()['id'] is not None

# 4. Test PATCH /inventory/<id> (Update item)
def test_update_item(client):
    update_data = {
        "price": 6.49,
        "quantity": 45
    }
    response = client.patch('/inventory/1', json=update_data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['price'] == 6.49
    assert json_data['quantity'] == 45

# 5. Test DELETE /inventory/<id> (Remove item)
def test_delete_item(client):
    response = client.delete('/inventory/2')
    assert response.status_code == 200
    
    # Confirm it is gone
    get_response = client.get('/inventory/2')
    assert get_response.status_code == 404

# 6. Test External API Proxy/Interaction Route
def test_external_search_found(client):
    response = client.get('/external-search?q=kitkat')
    assert response.status_code == 200
    assert response.get_json()['product_name'] == "KitKat Chunky"

def test_external_search_missing(client):
    response = client.get('/external-search?q=unknown_item_xyz')
    assert response.status_code == 404