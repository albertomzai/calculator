from flask import Flask

# Inicializar la aplicación Flask
app = Flask(__name__)
# Configuración mínima (puede incluir SECRET_KEY si se desea)
app.config['JSON_SORT_KEYS'] = False

# Importar las rutas para que se registren en la app
from . import routes