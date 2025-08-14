import pytest

# Ensure the project root is in PYTHONPATH for imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as c:
        yield c

def test_calculate_success(client):
    payload = {'expression': '5*8-3'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'result' in data
    assert data['result'] == 37

def test_calculate_invalid_expression(client):
    payload = {'expression': '5*/8'}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 400

def test_missing_expression_field(client):
    payload = {}
    response = client.post('/api/calculate', json=payload)
    assert response.status_code == 400