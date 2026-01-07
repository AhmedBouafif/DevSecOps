import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_health_check(client):
    """Test health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_check_boycott_product(client):
    """Test checking a product on the boycott list"""
    response = client.post('/check-product',
                          json={'product_name': 'Coca-Cola'})
    assert response.status_code == 200
    data = response.json
    assert data['is_boycott'] == True
    assert 'alternatives' in data
    assert len(data['alternatives']) > 0

def test_check_non_boycott_product(client):
    """Test checking a product not on the boycott list"""
    response = client.post('/check-product',
                          json={'product_name': 'Random Product'})
    assert response.status_code == 200
    data = response.json
    assert data['is_boycott'] == False

def test_empty_product_name(client):
    """Test with empty product name"""
    response = client.post('/check-product',
                          json={'product_name': ''})
    assert response.status_code == 400

def test_missing_product_name(client):
    """Test with missing product name"""
    response = client.post('/check-product', json={})
    assert response.status_code == 400
