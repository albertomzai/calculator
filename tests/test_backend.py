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

def test_calculate_division(client):
    response = client.post('/api/calculate', json={'expression': '10/2'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 5.0

def test_calculate_invalid_syntax(client):
    response = client.post('/api/calculate', json={'expression': '5 ** 2'})
    assert response.status_code == 400

def test_calculate_missing_expression(client):
    response = client.post('/api/calculate', json={})
    assert response.status_code == 400

def test_calculate_non_json(client):
    response = client.post('/api/calculate', data='not a json')
    assert response.status_code == 400