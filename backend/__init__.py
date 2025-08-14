"""Paquete backend del proyecto.

Expose la factory create_app para ser usada por la aplicación y por las pruebas."""

from .routes import create_app  # re‑exportar la fábrica
__all__ = ['create_app']