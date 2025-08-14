# app_pkg.py – proxy para que Pytest encuentre el paquete real
import os, sys

# Añadir al path la ruta donde está el paquete real (workspace/calculator)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'workspace', 'calculator'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Importar la factory del backend real
from app_pkg.backend import create_app  # noqa: E402,F401
__all__ = ['create_app']