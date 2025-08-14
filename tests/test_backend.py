import pytest

from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_calculate_success(client):
    payload = {'expression': '5*8-3'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'result' in data
    assert data['result'] == 37

def test_calculate_invalid_expression(client):
    payload = {'expression': '5++2'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_calculate_missing_expression(client):
    payload = {'wrong_key': '5+2'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_calculate_empty_expression(client):
    payload = {'expression': ''}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data