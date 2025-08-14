# Visión General del Proyecto
Este proyecto es una **calculadora web sencilla** que permite a los usuarios evaluar expresiones aritméticas básicas (sumas, restas, multiplicaciones y divisiones) directamente desde el navegador. La aplicación está compuesta por dos partes principales:

1. **Backend (Python/Flask)**  
   - Expone un endpoint `/api/calculate` que recibe una expresión en JSON, la evalúa de forma segura y devuelve el resultado.
   - Utiliza un *Blueprint* para organizar las rutas relacionadas con la calculadora.
   - Incluye lógica de validación para evitar caracteres no permitidos y manejo de errores HTTP.

2. **Frontend (HTML/CSS/JavaScript)**  
   - Un simple UI de 4×5 botones que permite introducir números, operadores y calcular el resultado.
   - Se comunica con el backend mediante `fetch` POST a `/api/calculate`.
   - Muestra resultados o mensajes de error en la pantalla del navegador.

El proyecto está pensado como una demostración de buenas prácticas básicas: separación de responsabilidades, validación segura de entrada y pruebas unitarias con Pytest.

---

# Arquitectura del Sistema
```mermaid
graph TD
    A[Cliente Web] -->|HTTP POST /api/calculate| B[Flask App]
    B --> C{Blueprint calc}
    C --> D[_safe_eval()]
    D --> E[Resultado numérico]
    E --> F[Respuesta JSON {result}]
```

- **Flask App**  
  - Se crea con `create_app()` que configura el static folder (`frontend`) y registra el *Blueprint*.
  - La raíz `/` sirve la página estática `index.html`.

- **Blueprint `calc_bp`**  
  - Ruta POST `/api/calculate`.
  - Valida que el cuerpo sea JSON y contenga la clave `expression`.
  - Llama a `_safe_eval()` para evaluar la expresión.

- **Función `_safe_eval(expr)`**  
  - Verifica que todos los caracteres pertenezcan al conjunto permitido (`0123456789+-*/(). `).
  - Evalúa la expresión con `eval` en un entorno restringido (`__builtins__: None`).

---

# Endpoints de la API

| Método | Ruta               | Parámetros de Entrada                         | Respuesta Exitosa | Código de Error | Mensaje |
|--------|--------------------|----------------------------------------------|-------------------|-----------------|---------|
| POST   | `/api/calculate`   | `{"expression": "<string>"}`                 | 200 OK            | 400             | Descripción del error |

### Ejemplo de solicitud
```bash
curl -X POST http://localhost:5000/api/calculate \
     -H "Content-Type: application/json" \
     -d '{"expression":"5*8-3"}'
```

### Respuesta exitosa
```json
{
  "result": 37
}
```

### Respuesta de error (ejemplo)
```json
{
  "message": "Expression contains invalid characters"
}
```

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <nombre_del_repositorio>
   ```

2. **Crear entorno virtual (opcional pero recomendado)**  
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate          # Windows
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**  
   ```bash
   python app.py
   ```
   La API estará disponible en `http://0.0.0.0:5000/` y el frontend en `http://localhost:5000/`.

5. **Ejecutar pruebas unitarias**  
   ```bash
   pytest tests/
   ```

---

# Flujo de Datos Clave

1. El usuario escribe una expresión en la interfaz.
2. JavaScript captura el evento del botón "=" y envía un POST a `/api/calculate` con `{"expression": "<exp>"}`.
3. Flask recibe la solicitud, valida JSON y presencia de `expression`.
4. Se llama a `_safe_eval()` que:
   - Comprueba caracteres válidos.
   - Evalúa la expresión en un entorno seguro.
5. Si la evaluación es correcta, se devuelve `{ "result": <valor> }` con código 200.
6. El frontend muestra el resultado o, en caso de error, el mensaje correspondiente.

---

# Extensiones Futuras (Opcional)

- **Soporte para funciones matemáticas** (`sin`, `cos`, `sqrt`) añadiendo un whitelist más amplio y utilizando la librería `math`.
- **Persistencia de historial**: guardar expresiones y resultados en una base de datos SQLite con SQLAlchemy.
- **Autenticación básica** para limitar el uso a usuarios registrados.
- **Interfaz móvil responsiva** usando frameworks como Bootstrap o TailwindCSS.
- **Implementar WebSocket** para cálculos en tiempo real o notificaciones de errores.