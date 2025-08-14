# Visión General del Proyecto

Este proyecto es una API ligera de **calculadora** construida con Flask. Su objetivo principal es recibir expresiones matemáticas simples en formato JSON y devolver el resultado evaluado. La aplicación está diseñada para ser minimalista, segura y fácil de desplegar tanto localmente como en entornos cloud.

- **Tecnologías principales:**  
  - Python 3.x  
  - Flask (microframework web)  
  - Blueprint para modularizar las rutas  
  - `eval` restringido para evaluar expresiones numéricas

- **Estructura del código:**  
  - Un único archivo `__init__.py` que contiene la aplicación Flask, el blueprint y la lógica de evaluación.  
  - Se sirve una página estática (`index.html`) desde la carpeta `frontend`.

El flujo de trabajo típico es: cliente → POST `/api/calculate` con JSON `{ "expression": "2+3*4" }` → servidor evalúa → responde con `{ "result": 14 }`.

---

# Arquitectura del Sistema

```
┌───────────────────────┐
│   Cliente (Browser)   │
└─────────────▲─────────┘
              │ HTTP POST
              │ /api/calculate
              ▼
        ┌─────────────────────┐
        │  Flask Application  │
        │  - Blueprint: calc  │
        │  - _safe_eval()     │
        └───────▲──────────────┘
                │ JSON Response
                ▼
          { "result": <value> }
```

## Componentes Clave

| Componente | Responsabilidad |
|------------|-----------------|
| **Flask App** | Orquesta la recepción de peticiones, envía respuestas y sirve archivos estáticos. |
| **Blueprint `calc_bp`** | Agrupa las rutas relacionadas con la calculadora (`/api/calculate`). |
| **Función `_safe_eval()`** | Valida y evalúa expresiones numéricas usando `eval` con un entorno restringido para evitar código arbitrario. |
| **Endpoint `/api/calculate`** | Recibe JSON, extrae la expresión, valida y devuelve el resultado o errores. |

---

# Endpoints de la API

## Tabla de Rutas

| Método | Ruta                 | Descripción                                      | Parámetros Entrada            | Respuesta Exitosa | Código de Error |
|--------|----------------------|--------------------------------------------------|------------------------------|-------------------|-----------------|
| POST   | `/api/calculate`     | Calcula una expresión matemática.               | `{"expression":"<string>"}`  | `200 OK: {"result": <number>}` | `400 Bad Request` (payload inválido o expresión no válida) |

### Ejemplo de Solicitud

```http
POST /api/calculate HTTP/1.1
Content-Type: application/json

{
  "expression": "(2 + 3) * 4 - 5 / 2"
}
```

### Respuesta Exitosa

```json
{
  "result": 15.5
}
```

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu-usuario/calculator-api.git
   cd calculator-api
   ```

2. **Crear entorno virtual (opcional pero recomendado)**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install Flask
   ```

4. **Estructura de carpetas**  
   Asegúrate de que exista una carpeta `frontend` con un archivo `index.html`. Si no la tienes, crea un mínimo:

   ```
   frontend/
     └─ index.html
   ```

5. **Ejecutar la aplicación**  
   ```bash
   export FLASK_APP=__init__.py
   flask run --host=0.0.0.0 --port=5000
   ```

   La API estará disponible en `http://localhost:5000/api/calculate` y el front‑end en `http://localhost:5000/`.

---

# Flujo de Datos Clave

1. **Cliente** envía una petición HTTP POST a `/api/calculate` con un cuerpo JSON que contiene la clave `"expression"`.
2. **Flask** recibe la solicitud, verifica que sea JSON y extrae el valor de `"expression"`.
3. La expresión se pasa a `_safe_eval()`:
   - Se valida que solo contenga caracteres permitidos (`0‑9`, `+−*/().`).
   - Se evalúa con `eval` en un entorno sin builtins.
4. Si la evaluación es exitosa, Flask devuelve un JSON con el resultado: `{ "result": <valor> }`.
5. En caso de error (JSON inválido, expresión mal formada o caracteres prohibidos), se devuelve un 400 con descripción del problema.

---

# Extensiones Futuras

| Área | Posible Mejora |
|------|----------------|
| **Seguridad** | Reemplazar `eval` por una biblioteca como `asteval` o `sympy` para mayor robustez. |
| **Persistencia** | Añadir un endpoint `/history` que almacene y retorne las últimas expresiones evaluadas en una base de datos SQLite. |
| **Autenticación** | Implementar JWT para limitar el uso a usuarios autenticados. |
| **Front‑end** | Desarrollar una SPA con React/Vue que consuma la API y muestre un historial interactivo. |

---