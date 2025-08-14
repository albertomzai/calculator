"""Root application entry point."""

from backend import create_app

__all__ = ['app']

app = create_app()