"""Pruebas de integración para el endpoint /api/calculate."""

import json
from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_calculate_success(client):
    payload = {'expression': '5*8-3'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 37

def test_calculate_invalid_expression(client):
    payload = {'expression': '5*/2'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 400