import pytest

from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_successful_calculation(client):
    response = client.post('/api/calculate', json={'expression': '5*8-3'})
    assert response.status_code == 200
    assert response.get_json() == {'result': 37}

def test_empty_expression(client):
    response = client.post('/api/calculate', json={'expression': ''})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_missing_expression_key(client):
    response = client.post('/api/calculate', json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_invalid_syntax(client):
    response = client.post('/api/calculate', json={'expression': '5*/2'})
    assert response.status_code == 400
    assert 'error' in response.get_json()