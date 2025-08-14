# app_pkg.__init__

# Import the backend factory without causing circular imports.
from .backend import create_app as _create_app

__all__ = ['_create_app']