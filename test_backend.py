import pytest
from backend import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_root_returns_html(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<html' in response.data
    assert b'Calculadora API' in response.data

def test_calculate_success(client):
    payload = {"expression": "5*8-3"}
    resp = client.post('/api/calculate', json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'result' in data
    assert data['result'] == 37

def test_calculate_invalid(client):
    payload = {"expression": "5*/8"}
    resp = client.post('/api/calculate', json=payload)
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data