"""Unit tests for the backend API."""


import pytest

from flask import json


@pytest.fixture

def client():

    from app import app as flask_app

    with flask_app.test_client() as client:

        yield client


def test_calculate_success(client):

    response = client.post("/api/calculate", json={"expression": "5*8-3"})

    assert response.status_code == 200

    data = json.loads(response.data)

    assert data["result"] == 37


def test_calculate_invalid_expression(client):

    # Expression ends with an operator which is invalid.
        response = client.post("/api/calculate", json={"expression": "5+"})

    assert response.status_code == 400

    data = json.loads(response.data)

    assert "error" in data


def test_calculate_missing_expression(client):

    response = client.post("/api/calculate", json={})

    assert response.status_code == 400

    data = json.loads(response.data)

    assert "error" in data