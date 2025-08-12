import pytest

from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

class TestCalculateEndpoint:

    def test_valid_expression(self, client):
        response = client.post('/api/calculate', json={'expression': '5*8-3'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == 37

    def test_invalid_expression(self, client):
        response = client.post('/api/calculate', json={'expression': '5*/8'})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_missing_expression_key(self, client):
        response = client.post('/api/calculate', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data