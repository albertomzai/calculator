"""Test suite for the calculator backend API."""

import json
import pytest

from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_calculate_success(client):
    payload = {"expression": "5*8-3"}
    response = client.post("/api/calculate", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] == 37

def test_calculate_invalid_expression(client):
    payload = {"expression": "5*/2"}
    response = client.post("/api/calculate", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400

def test_missing_expression_field(client):
    payload = {"expr": "1+1"}
    response = client.post("/api/calculate", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400