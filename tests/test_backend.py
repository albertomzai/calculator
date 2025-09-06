import pytest
from backend import create_app

def test_calculate():
    app = create_app()
    client = app.test_client()
    response = client.post('/api/calculate', json={'expression': '5+3'})
    assert response.status_code == 200
    assert response.json['result'] == 8