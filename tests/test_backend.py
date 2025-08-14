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
    assert 'result' in data
    assert data['result'] == 37

def test_calculate_invalid_expression(client):
    response = client.post('/api/calculate', json={'expression': '5**'})
    assert response.status_code == 400

def test_missing_expression_key(client):
    response = client.post('/api/calculate', json={})
    assert response.status_code == 400

def test_non_json_request(client):
    response = client.post('/api/calculate', data='not json')
    assert response.status_code == 400