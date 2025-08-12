We need to produce markdown. Let's craft sections accordingly.# Visión General del Proyecto

Este proyecto implementa una **calculadora web** sencilla que permite evaluar expresiones matemáticas básicas a través de un backend Flask y un frontend estático en HTML/JavaScript. El flujo típico es el siguiente:

1. El usuario escribe una expresión matemática (por ejemplo, `5*8-3`) usando la interfaz gráfica.
2. Al pulsar “=”, el cliente envía la expresión al endpoint `/api/calculate` mediante una petición **POST** con JSON.
3. El servidor analiza y evalúa la expresión de forma segura utilizando el módulo `ast`, evitando la ejecución de código arbitrario.
4. La respuesta devuelve el resultado en formato JSON, que se muestra en la pantalla.

El proyecto está pensado para ser ligero, fácil de desplegar y extensible a futuro (por ejemplo, añadir más operaciones o una capa de autenticación).

---

# Arquitectura del Sistema

## Estructura de paquetes

```
.
├── app.py                    # Punto de entrada principal
├── requirements.txt          # Dependencias
└── backend/
    ├── __init__.py           # Factory y configuración de Flask
    ├── app.py                # Instancia de la aplicación
    └── routes.py             # Endpoints API
```

- **`app.py`**: Ejecuta el servidor en `0.0.0.0` con puerto configurable por variable de entorno.
- **`backend/__init__.py`**: Crea y configura la app Flask, registra blueprints y sirve el frontend estático (`index.html`) desde `frontend/`.
- **`backend/routes.py`**: Contiene la lógica del endpoint `/calculate`.

## Diagrama Mermaid

```mermaid
graph TD;
    A[Cliente Web] -->|POST /api/calculate| B[Flask App];
    B --> C[Parse Expression (AST)];
    C --> D[Evaluate Safe Ops];
    D --> E[Return Result JSON];
    E -->|200 OK| A;
```

---

# Endpoints de la API

| Método | Ruta               | Descripción                                 | Parámetros Entrada                        | Respuesta Exitosa                     |
|--------|--------------------|---------------------------------------------|-------------------------------------------|---------------------------------------|
| POST   | `/api/calculate`   | Evalúa una expresión matemática segura.     | `{"expression": "string"}`                | `200 OK`<br>`{ "result": number }`    |

## Validaciones

- **Tipo**: El campo `expression` debe ser un string; de lo contrario, se devuelve `400 Bad Request`.
- **Sintaxis/Operadores**: Se permiten solo operadores aritméticos básicos (`+`, `-`, `*`, `/`, `**`) y números. Cualquier otra sintaxis genera `422 Unprocessable Entity` con mensaje `"Invalid expression"`.
- **División por cero**: Devuelve `422` con mensaje `"division by zero"`.

## Ejemplo de respuesta

```json
{
  "result": 37
}
```

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone <url_del_repositorio>
   cd <directorio_del_proyecto>
   ```

2. **Crear entorno virtual (opcional pero recomendado)**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**  
   ```bash
   python app.py
   ```
   La API estará disponible en `http://0.0.0.0:5000/`.

5. **Probar los tests** (opcional)  
   ```bash
   pytest
   ```

---

# Flujo de Datos Clave

1. **Entrada del usuario** → Botones del frontend generan una cadena (`expression`).
2. **Petición HTTP** → Cliente envía `POST /api/calculate` con JSON.
3. **Parser AST** → `ast.parse(expr, mode='eval')` convierte la expresión en árbol sintáctico.
4. **Evaluación segura**  
   - Recursión sobre nodos: `Num`, `Constant`, `BinOp`, `UnaryOp`.  
   - Operadores permitidos definidos en `_ALLOWED_OPERATORS`.
5. **Resultado** → Se serializa a JSON y se envía de vuelta al cliente.
6. **Renderizado** → El script JavaScript actualiza el display con el resultado o muestra un error.

---

# Extensiones Futuras (Opcional)

- **Soporte para funciones matemáticas** (`sin`, `cos`, `sqrt`) mediante la extensión del AST y una tabla de funciones seguras.
- **Persistencia de historial**: Guardar expresiones y resultados en una base de datos SQLite o PostgreSQL, con endpoints adicionales `/history`.
- **Autenticación JWT**: Restringir el acceso a la API para usuarios registrados.
- **API Swagger/OpenAPI**: Generar documentación automática del endpoint `calculate`.
- **Frontend React/Vue**: Reemplazar el HTML/JS estático por un SPA más robusto y con pruebas end-to-end.

---