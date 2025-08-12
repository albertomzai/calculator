# tests/test_calculator.py
import pytest
from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

# Valid expression tests
@pytest.mark.parametrize(
    "expression,expected",
    [
        ("2+3", 5),
        ("10-4", 6),
        ("5*8", 40),
        ("20/4", 5.0),
        ("1+2*3-4/2", 1 + 2 * 3 - 4 / 2),
        ("-5+3", -2),
    ],
)
def test_calculate_success(client, expression, expected):
    response = client.post("/api/calculate", json={"expression": expression})
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] == expected

# Invalid input tests
@pytest.mark.parametrize(
    "payload,expected_status",
    [
        ({}, 400),  # missing expression key
        ({"expression": None}, 400),
        ({"expression": ""}, 400),
        ({"expression": "   "}, 400),
        ({"expression": "2+"}, 400),  # syntax error
        ({"expression": "10/0"}, 400),  # division by zero handled as EvalError
    ],
)
def test_calculate_invalid(client, payload, expected_status):
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == expected_status
