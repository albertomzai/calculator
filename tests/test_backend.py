import pytest

from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_valid_expression(client):
    response = client.post('/api/calculate', json={'expression': '5*8-3'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 37

def test_missing_expression_field(client):
    response = client.post('/api/calculate', json={})
    assert response.status_code == 400
    assert 'Missing' in response.get_json()['error']

def test_non_string_expression(client):
    response = client.post('/api/calculate', json={'expression': 1234})
    assert response.status_code == 400
    assert 'must be a string' in response.get_json()['error']

def test_syntax_error_expression(client):
    response = client.post('/api/calculate', json={'expression': '5+*2'})
    assert response.status_code == 422
    assert 'Invalid syntax' in response.get_json()['error']

def test_division_by_zero(client):
    response = client.post('/api/calculate', json={'expression': '10/0'})
    assert response.status_code == 422
    assert 'Division by zero' in response.get_json()['error']