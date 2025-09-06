import pytest
from backend import create_app

@pytest.fixturedef client():
    app = create_app()
    with app.test_client() as testing_client:
        yield testing_client

@pytest.mark.parametrize('expression, expected', [
    ('5*8-3', 37),
    ('10/2', 5),
    ('(4+6)*2', 20),
])def test_calculate_endpoint(client, expression, expected):
    response = client.post('/api/calculate', json={'expression': expression}),
    assert response.status_code == 200
    result = response.get_json()['resultado']
    assert result == expected