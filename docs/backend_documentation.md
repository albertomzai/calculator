# Visión General del Proyecto

El proyecto es una API sencilla de cálculo aritmético construida con **Flask** en Python. Su objetivo principal es recibir expresiones matemáticas en formato string a través de un endpoint `/api/calculate` y devolver el resultado numérico correspondiente. La aplicación también sirve archivos estáticos (probablemente una interfaz web) desde la carpeta `frontend`.

### Características principales
- **Evaluación segura**: El motor interno `_safe_eval` restringe los caracteres permitidos y desactiva todos los builtins de Python, evitando la ejecución de código arbitrario.
- **Validaciones exhaustivas**: Se comprueba que el payload contenga un campo `expression`, que sea una cadena no vacía y que solo incluya operadores aritméticos básicos.
- **Manejo de errores**: Utiliza códigos HTTP 400 con mensajes descriptivos cuando la entrada es inválida.
- **Arquitectura modular**: La lógica de cálculo está encapsulada en un Blueprint (`calc_bp`), lo que facilita su extensión o reemplazo.

El flujo de trabajo típico para un cliente:
1. Enviar una petición `POST /api/calculate` con JSON `{ "expression": "2 + 3 * (4 - 1)" }`.
2. El servidor valida y evalúa la expresión.
3. Se devuelve `{ "result": 11 }`.

---

# Arquitectura del Sistema

El sistema se compone de los siguientes componentes:

| Componente | Descripción |
|------------|-------------|
| **Flask App** | Instancia principal que gestiona rutas, configuración y servir archivos estáticos. |
| **Blueprint `calc_bp`** | Encapsula la lógica de cálculo y define el endpoint `/api/calculate`. |
| **Función `_safe_eval`** | Función interna que valida y evalúa expresiones aritméticas en un entorno restringido. |
| **Factory `create_app()`** | Patrón de fábrica para crear instancias configurables del app, útil en pruebas o despliegues múltiples. |

## Diagrama Mermaid

```mermaid
flowchart TD
    A[Client] --> B{POST /api/calculate}
    B --> C[Flask App]
    C --> D[calc_bp Blueprint]
    D --> E[_safe_eval]
    E --> F[Result or Error]
    F --> G[JSON Response]
    H[GET /] --> I[Static Files (index.html)]
```

---

# Endpoints de la API

| Método | Ruta | Parámetros | Descripción |
|--------|------|------------|-------------|
| **POST** | `/api/calculate` | `application/json`: `{ "expression": "<string>" }` | Calcula el resultado de una expresión aritmética segura. |
| **GET** | `/` | N/A | Sirve la página principal (`index.html`) desde la carpeta estática. |

## Respuestas

- **200 OK**  
  ```json
  { "result": <number> }
  ```
- **400 Bad Request** (expresión inválida, faltante o con caracteres no permitidos)  
  ```json
  { "message": "<error description>" }
  ```

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu_usuario/calculator-backend.git
   cd calculator-backend
   ```

2. **Crear entorno virtual** (opcional pero recomendado)  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```
   > Si no existe `requirements.txt`, instala Flask directamente:
   > ```bash
   > pip install flask
   > ```

4. **Ejecutar la aplicación**  
   ```bash
   export FLASK_APP=__init__.py  # o set FLASK_APP=__init__.py en Windows
   flask run
   ```
   La API estará disponible en `http://127.0.0.1:5000`.

5. **Probar el endpoint** (ejemplo con `curl`)  
   ```bash
   curl -X POST http://127.0.0.1:5000/api/calculate \
        -H "Content-Type: application/json" \
        -d '{"expression": "2 + 3 * (4 - 1)"}'
   ```

---

# Flujo de Datos Clave

```
Client ──► POST /api/calculate
          │      { "expression": "..."}
          ▼
     Flask App
          │
          ▼
    calc_bp Blueprint
          │
          ▼
   _safe_eval(expression)
          │  (validación y eval)
          ▼
   Result or Error
          │
          ▼
   JSON Response
```

- **Entrada**: `expression` string desde el cuerpo JSON.
- **Procesamiento**:
  - Validar caracteres permitidos (`0123456789+-*/. ()`).
  - Evaluar con `eval` en un entorno sin builtins.
  - Verificar que el resultado sea numérico.
- **Salida**: JSON con campo `result` o error descriptivo.

---

# Extensiones Futuras

| Área | Posible Mejora |
|------|----------------|
| **Seguridad** | Implementar una librería de parsing de expresiones (p.ej., `asteval`) para evitar el uso de `eval`. |
| **Soporte Matemático** | Añadir funciones trigonométricas, exponenciación y manejo de constantes (`pi`, `e`). |
| **Persistencia** | Guardar historial de cálculos en una base de datos SQLite o PostgreSQL. |
| **Autenticación** | Proteger el endpoint con JWT para limitar el uso a usuarios registrados. |
| **Documentación API** | Generar Swagger/OpenAPI automáticamente usando `flask-restx` o `connexion`. |

---