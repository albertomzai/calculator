# tests/test_backend.py
import pytest
from app_pkg.backend import app as flask_app  # Importa explícitamente desde app_pkg

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_calculate_success(client):
    response = client.post('/api/calculate', json={'expression': '5*8-3'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 37

def test_calculate_division(client):
    response = client.post('/api/calculate', json={'expression': '10/2'})
    assert response.status_code == 200
    assert response.get_json()['result'] == 5.0

def test_invalid_expression(client):
    response = client.post('/api/calculate', json={'expression': '5**2'})
    assert response.status_code == 400

def test_missing_expression_key(client):
    response = client.post('/api/calculate', json={})
    assert response.status_code == 400

def test_non_json_request(client):
    response = client.post('/api/calculate', data='not json')
    assert response.status_code == 400