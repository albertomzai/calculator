import pytest

from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_calculate_valid(client):
    response = client.post("/api/calculate", json={"expression": "5*8-3"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 37

def test_calculate_invalid_syntax(client):
    response = client.post("/api/calculate", json={"expression": "5**2"})
    assert response.status_code == 400

def test_calculate_missing_field(client):
    response = client.post("/api/calculate", json={})
    assert response.status_code == 400

def test_calculate_non_string(client):
    response = client.post("/api/calculate", json={"expression": 123})
    assert response.status_code == 400