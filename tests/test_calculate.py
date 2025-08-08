# tests/test_calculate.py
"""Pruebas unitarias para la API de cálculo."""

import pytest
from app import create_app

@pytest.fixture
def client():
    """Crea un test_client aislado para las pruebas."""
    app = create_app()
    with app.test_client() as client:
        yield client


def test_calculate_success(client):
    response = client.post("/api/calculate", json={"expression": "5*8-3"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 37


def test_calculate_division_by_zero(client):
    response = client.post("/api/calculate", json={"expression": "10/0"})
    assert response.status_code == 400
    assert "División por cero" in response.get_data(as_text=True)


def test_calculate_invalid_syntax(client):
    response = client.post("/api/calculate", json={"expression": "5**"})
    assert response.status_code == 400
    assert "Expresión inválida" in response.get_data(as_text=True)


def test_calculate_missing_expression(client):
    response = client.post("/api/calculate", json={})
    assert response.status_code == 400
    assert "'expression'" in response.get_data(as_text=True)
