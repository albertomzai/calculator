import pytest
from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_calculate_success(client):
    response = client.post('/api/calculate', json={'expression': '5*8-3'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'result' in data
    assert data['result'] == 37

def test_calculate_invalid_chars(client):
    response = client.post('/api/calculate', json={'expression': '5+8a-3'})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_calculate_division_by_zero(client):
    response = client.post('/api/calculate', json={'expression': '10/0'})
    assert response.status_code == 400
    assert 'Division by zero' in response.get_json()['error']