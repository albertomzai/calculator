# run.py
"""Script de entrada para ejecutar la aplicación Flask."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Se ejecuta en todas las interfaces de red, puerto 5000.
    app.run(host="0.0.0.0", port=5000)
