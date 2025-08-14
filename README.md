# Visión General del Proyecto

Este repositorio alberga una **calculadora web** sencilla pero robusta que separa la lógica de cálculo en el backend y la presentación en un único archivo HTML.  
La aplicación se ejecuta con Flask y expone una API REST para evaluar expresiones matemáticas de forma segura, mientras que la interfaz de usuario funciona como una SPA (Single Page Application) construida con HTML/CSS/JavaScript puro.

## Estructura del código

- `app.py` – Punto de entrada que arranca el servidor Flask.  
- `backend/` – Paquete que contiene la fábrica de la app (`create_app`) y las rutas API. Dentro se encuentra `routes.py`, donde se define el endpoint `/api/calculate` y la función recursiva `_eval_expr` que utiliza el módulo `ast` para evaluar únicamente operaciones aritméticas permitidas.  
- `frontend/` – Carpeta con un único archivo `index.html`. Este documento incluye la lógica de la calculadora, los estilos y las llamadas a la API.  
- `tests/` – Pruebas unitarias con Pytest que verifican el correcto funcionamiento del endpoint y la validación de entrada.

# Arquitectura del Sistema

```mermaid
flowchart TD
    A[Flask App] -->|register_blueprint| B(BluePrint "api")
    B --> C[/api/calculate (POST)]
    C --> D{_eval_expr}
    D -->|returns result| E[JSON Response]
```

- **Flask App**: Punto central que configura la ruta estática y registra el blueprint de la API.  
- **Blueprint “api”**: Agrupa todas las rutas relacionadas con la funcionalidad del backend.  
- **Endpoint `/api/calculate`**: Recibe una expresión matemática en JSON, valida su tipo, la analiza con `ast.parse`, evalúa con `_eval_expr` y devuelve el resultado o un error.  
- **Evaluador (`_eval_expr`)**: Recorre de forma segura el árbol sintáctico abstracto (AST) permitiendo solo operadores aritméticos básicos (`+ - * / **`) y números.

# Endpoints de la API

| Método | Ruta              | Descripción                                                                 |
|--------|-------------------|-----------------------------------------------------------------------------|
| POST   | `/api/calculate`  | Evalúa una expresión matemática enviada en JSON bajo el campo `expression`. Responde con `{ "result": <valor> }` o un error. |

**Ejemplo de petición**

```bash
curl -X POST http://localhost:5000/api/calculate \
     -H "Content-Type: application/json" \
     -d '{"expression":"5*8-3"}'
```

**Respuesta exitosa**

```json
{
  "result": 37
}
```

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu_usuario/calc-web.git
   cd calc-web
   ```

2. **Crear un entorno virtual (opcional pero recomendado)**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**  
   ```bash
   python app.py
   ```

5. **Acceder en el navegador**  
   Abre `http://localhost:5000`.

# Flujo de Datos Clave

1. El usuario escribe una expresión en la calculadora web y pulsa “=”.  
2. JavaScript captura el valor, lo envía a `/api/calculate` vía `fetch` con método POST.  
3. Flask recibe la petición, extrae `expression`, valida su tipo y parsea con `ast.parse`.  
4. `_eval_expr` recorre el AST evaluando solo operadores permitidos (`+ - * / **`).  
5. El resultado (o error) se devuelve como JSON a la SPA.  
6. La SPA muestra el resultado en la pantalla.

# Extensiones Futuras

- **Persistencia de historial**: Añadir una base de datos SQLite para almacenar las expresiones evaluadas por cada usuario.  
- **Autenticación**: Implementar JWT o sesiones para que los usuarios puedan iniciar sesión y ver su historial personal.  
- **Soporte de funciones trigonométricas**: Extender `_eval_expr` para aceptar `sin`, `cos`, `tan`, etc., usando el módulo `math`.  
- **UI React/Vue**: Migrar la SPA a un framework moderno para una experiencia más rica y modular.