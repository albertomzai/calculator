import pytest

from backend.app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_calculate_valid(client):
    response = client.post('/api/calculate', json={'expression': '5*8-3'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 37

def test_calculate_invalid_type(client):
    response = client.post('/api/calculate', json={'expression': 123})
    assert response.status_code == 400

def test_calculate_syntax_error(client):
    response = client.post('/api/calculate', json={'expression': '5*/2'})
    assert response.status_code == 422

def test_division_by_zero(client):
    response = client.post('/api/calculate', json={'expression': '10/0'})
    assert response.status_code == 422