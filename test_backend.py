# test_backend.py
import pytest
from backend import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_root_route(client):
    response = client.get('/')
    assert response.status_code == 200
    # Se espera que devuelva un archivo html, por lo que el contenido no debe estar vacío
    assert b"<html" in response.data or len(response.data) > 0

def test_calculate_success(client):
    payload = {'expression': '5*8-3'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'result' in data
    assert data['result'] == 37

def test_calculate_invalid_expr(client):
    payload = {'expression': '5*/2'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_calculate_missing_payload(client):
    response = client.post('/api/calculate')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
