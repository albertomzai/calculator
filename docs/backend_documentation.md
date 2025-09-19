# Visión General del Proyecto

El proyecto es una API web sencilla construida con **Flask** que expone un único endpoint `/api/calculate`. Su objetivo principal es recibir expresiones aritméticas en formato JSON, evaluarlas de manera segura y devolver el resultado. Además, la aplicación sirve una interfaz frontend estática (ubicada en la carpeta `frontend`) a través del mismo servidor Flask.

## Características principales

- **Evaluación segura**: Se emplea el módulo `ast` para parsear la expresión y se restringe estrictamente a los operadores binarios básicos (`+`, `-`, `*`, `/`). Cualquier otro nodo produce un error.
- **API RESTful mínima**: Un solo endpoint POST que devuelve JSON con el resultado o un mensaje de error descriptivo.
- **Frontend estático**: El servidor Flask sirve archivos estáticos, facilitando la integración con cualquier SPA ligera sin necesidad de un servidor separado.

---

# Arquitectura del Sistema

El proyecto sigue una arquitectura monolítica ligera basada en Flask. La estructura de paquetes es la siguiente:

```
project/
│
├── app.py                # Punto de entrada para ejecutar la aplicación
├── __init__.py           # Fábrica de la aplicación y configuración
├── routes.py             # Blueprint con las rutas API
└── requirements.txt      # Dependencias del proyecto
```

## Diagrama Mermaid

```mermaid
flowchart TD
    A[app.py] --> B{create_app}
    B --> C[Flask App]
    C --> D[api_bp (routes.py)]
    C --> E[/] -> F[frontend/index.html]
    D --> G[/api/calculate] --> H[POST JSON] --> I[_safe_eval] --> J[result]
```

---

# Endpoints de la API

| Método | Ruta            | Parámetros de Entrada          | Respuesta Exitosa | Código de Estado | Descripción |
|--------|-----------------|--------------------------------|-------------------|------------------|-------------|
| POST   | `/api/calculate` | `{"expression": "<string>"}`  | `{"result": <number>}` | 200 OK | Evalúa la expresión aritmética y devuelve el resultado. |
|        |                 |                                | `{"message": "error"}` | 400 Bad Request | Si falta el campo o la expresión es inválida, se devuelve un mensaje de error descriptivo. |

### Ejemplo de solicitud

```http
POST /api/calculate HTTP/1.1
Content-Type: application/json

{
  "expression": "3 + 4 * (2 - 1)"
}
```

### Ejemplo de respuesta

```json
{
  "result": 7
}
```

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <nombre_del_directorio>
   ```

2. **Crear un entorno virtual (opcional pero recomendado)**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación en modo desarrollo**  
   ```bash
   python app.py
   ```
   La API estará disponible en `http://0.0.0.0:5000/api/calculate` y el frontend en `http://0.0.0.0:5000/`.

5. **Ejecutar pruebas (si se incluyen)**  
   ```bash
   pytest
   ```

---

# Flujo de Datos Clave

1. **Cliente** envía una petición POST a `/api/calculate` con un cuerpo JSON que contiene el campo `expression`.
2. Flask recibe la solicitud y dirige la ruta al blueprint `api_bp`.
3. La función `_safe_eval` procesa la expresión:
   - Se parsea usando `ast.parse`.
   - Un visitante de AST valida cada nodo (solo permite binarios básicos y números).
   - Si la validación pasa, se compila y evalúa con un entorno restringido (`__builtins__` deshabilitado).
4. El resultado numérico es empaquetado en JSON y devuelto al cliente.
5. En caso de error (syntax, operador no permitido, valor no numérico), Flask responde con `400 Bad Request` y un mensaje descriptivo.

---

# Extensiones Futuras

| Área | Posible Mejora | Beneficio |
|------|----------------|-----------|
| **Seguridad** | Añadir autenticación JWT para proteger el endpoint. | Evita uso indebido de la API. |
| **Validaciones** | Soportar funciones matemáticas (`sqrt`, `pow`) con un whitelist controlado. | Ampliar funcionalidad sin comprometer seguridad. |
| **Documentación** | Generar OpenAPI/Swagger automáticamente usando Flask-RESTX o similar. | Facilita consumo por terceros y pruebas automáticas. |
| **Testing** | Implementar pruebas unitarias para `_safe_eval` con casos de borde (p.ej., división por cero). | Garantiza estabilidad ante cambios futuros. |

---