import pytest

from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_calculate_success(client):
    response = client.post('/api/calculate', json={'expression': '5*8-3'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 37

def test_calculate_invalid_syntax(client):
    response = client.post('/api/calculate', json={'expression': '5**'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'Invalid syntax' in data['error']

def test_calculate_missing_expression(client):
    response = client.post('/api/calculate', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'Missing or empty' in data['error']