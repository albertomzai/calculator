# Visión General del Proyecto

El proyecto es una **calculadora web** que separa la lógica de cálculo en el backend.

**Objetivo principal:** Exponer un único endpoint RESTful que reciba una expresión matemática como cadena y devuelva su resultado. El frontend, implementado como una SPA en `index.html`, consume este servicio para mostrar resultados al usuario.

## Flujo de Datos Clave

1. El usuario escribe la expresión en la pantalla de la calculadora (frontend).
2. Al pulsar el botón **=**, se envía una petición **POST** a `/api/calculate` con el cuerpo `{ "expression": "5*8-3" }`.
3. Flask recibe la solicitud, valida y evalúa la expresión de forma segura usando `ast`.
4. El resultado (o un error) se devuelve en JSON: `{ "result": 37 }` o `{ "error": "division by zero" }`.

# Arquitectura del Sistema

La arquitectura sigue el patrón **Modelo-Vista-Controlador** simplificado:

| Componente | Responsabilidad | Tecnología |
|------------|-----------------|------------|
| Frontend   | UI y gestión de eventos | HTML5, CSS3, JavaScript ES6 |
| Backend    | Exposición de API REST | Flask (Python) |

El backend no utiliza base de datos; la lógica de cálculo es volátil y se procesa en memoria.

# Endpoints de la API

## Tabla de Endpoints

| Método | Ruta | Descripción | Payload | Respuesta | Código de Estado |
|--------|------|-------------|---------|-----------|------------------|
| POST   | `/api/calculate` | Evalúa una expresión matemática | `{ "expression": "<string>" }` | `{ "result": <number> }` o `{ "error": "<mensaje>" }` | 200 (OK), 400 (Bad Request), 422 (Unprocessable Entity) |

### Esquema de Petición

```json
{
  "expression": "5*8-3"
}   
```

### Respuestas Posibles

- **200 OK**

```json
{
  "result": 37
}   
```

- **400 Bad Request** (payload inválido)

```json
{
  "error": "'expression' must be a string"
}   
```

- **422 Unprocessable Entity** (expresión no válida o error de cálculo)

```json
{
  "error": "Invalid expression"
}   
```
```

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/albertomzai/calculator.git
   cd calculator
   ```

2. **Crear un entorno virtual (opcional pero recomendado)**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**:

   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

5. **Acceder a la calculadora**: Navegar a `http://localhost:5000` en un navegador web.

# Extensiones Futuras

- **Persistencia de historial**: Añadir una base de datos ligera (SQLite) para almacenar las expresiones y resultados anteriores.
- **Soporte avanzado de funciones**: Incluir operaciones trigonométricas, logaritmos, etc., con validación segura.
- **Autenticación y control de acceso**: Implementar JWT o sesiones para usuarios registrados que puedan guardar su historial personal.
- **Internationalización (i18n)**: Soportar múltiples idiomas en la interfaz.
- **Testing automatizado**: Añadir pruebas unitarias y de integración tanto para el backend como para el frontend.