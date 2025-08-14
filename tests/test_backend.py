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
    assert data['result'] == 37

def test_calculate_missing_expression(client):
    response = client.post('/api/calculate', json={})
    assert response.status_code == 400

def test_calculate_invalid_expr(client):
    response = client.post('/api/calculate', json={'expression': '5**8'})
    assert response.status_code == 400