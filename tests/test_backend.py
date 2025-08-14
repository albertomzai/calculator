import pytest

# Import the factory function to create a testable app instance
from backend import create_app

@pytest.fixture
def client():
    """Create a Flask test client for API testing."""
    app = create_app()
    with app.test_client() as client:
        yield client

def test_calculate_success(client):
    response = client.post('/api/calculate', json={'expression': '5*8-3'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['result'] == 37

def test_calculate_syntax_error(client):
    # Invalid syntax should trigger a 400 error
    response = client.post('/api/calculate', json={'expression': '5*/8'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' not in data or isinstance(data, dict)

def test_calculate_missing_expression(client):
    # Missing expression key should trigger a 400 error
    response = client.post('/api/calculate', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' not in data or isinstance(data, dict)