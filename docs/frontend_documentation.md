# Visión General del Proyecto

Esta aplicación es una **calculadora web** sencilla que permite a los usuarios introducir expresiones aritméticas y obtener el resultado de forma inmediata. El front‑end está construido con HTML5, Bootstrap 5 para la estética y un pequeño script JavaScript que gestiona la interacción con la interfaz y se comunica con una API RESTful ubicada en `/api/calculate`. La arquitectura sigue un patrón **cliente‑servidor** donde:

- **Cliente**: navegador del usuario; renderiza el UI, captura eventos de los botones y envía peticiones HTTP al servidor.
- **Servidor**: expone un endpoint único (`POST /api/calculate`) que recibe una expresión matemática en formato JSON, la evalúa de forma segura y devuelve el resultado o un mensaje de error.

El objetivo principal es demostrar cómo separar la lógica de negocio (evaluación de expresiones) del UI, manteniendo una comunicación clara a través de HTTP y JSON. La aplicación está pensada para ser ligera, fácil de desplegar y extensible con nuevas funcionalidades matemáticas o mejoras en la interfaz.

---

# Arquitectura del Sistema

## Componentes Principales

| Componente | Descripción |
|------------|-------------|
| **Frontend** | Página HTML servida al navegador; incluye Bootstrap 5, estilos CSS personalizados y un script JavaScript que controla los botones de la calculadora. |
| **API REST** | Endpoint `POST /api/calculate` que recibe `{ expression: string }`, evalúa la expresión y devuelve `{ result: number }`. |
| **Evaluador Matemático** | Lógica del servidor encargada de parsear y calcular la expresión sin usar `eval()` por razones de seguridad. |

## Diagrama Mermaid

```mermaid
graph TD
    A[Usuario] -->|HTTP GET| B[Servidor - index.html]
    B --> C{Cliente}
    C --> D[Botones (7,8,...,=)]
    D --> E[Script JS]
    E -->|POST /api/calculate| F[API REST]
    F --> G[Evaluador Matemático]
    G -->|Resultado| F
    F -->|JSON {result}| E
    E -->|Mostrar en pantalla| C
```

---

# Endpoints de la API

## `POST /api/calculate`

### Descripción
Evalúa una expresión aritmética enviada por el cliente y devuelve el resultado.

### Request

| Campo | Tipo   | Requerido | Descripción                           |
|-------|--------|-----------|--------------------------------------|
| expression | string | Sí | Expresión matemática válida (ej. `"3+4*2"`). |

**Ejemplo de cuerpo JSON**

```json
{
  "expression": "12 / (2 + 1) * 5"
}
```

### Response

- **200 OK**

  ```json
  {
    "result": 20
  }
  ```

- **400 Bad Request**

  ```json
  {
    "error": "Expresión inválida: syntax error near '+'"
  }
  ```

- **500 Internal Server Error**

  ```json
  {
    "error": "Error interno al procesar la expresión."
  }
  ```

### Reglas de Validación

| Regla | Descripción |
|-------|-------------|
| Solo operadores aritméticos básicos (`+`, `-`, `*`, `/`) y paréntesis. |
| Los números pueden ser enteros o flotantes. |
| Se rechazan expresiones vacías, caracteres no permitidos o división por cero. |

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tuusuario/calculadora-web.git
   cd calculadora-web
   ```

2. **Instalar dependencias del servidor (Node.js + Express)**  
   ```bash
   npm install
   ```

3. **Iniciar el servidor**  
   ```bash
   node server.js
   ```
   El servidor escuchará en `http://localhost:3000`.

4. **Abrir la aplicación**  
   Navega a `http://localhost:3000` en tu navegador.

---

# Flujo de Datos Clave

1. **Entrada del Usuario**  
   - Los botones con atributo `data-value` añaden caracteres al campo `expressionDisplay`.
2. **Solicitud al Servidor**  
   - Al pulsar “=”, el script envía un `POST /api/calculate` con `{ expression: <texto> }`.
3. **Procesamiento en el Servidor**  
   - El endpoint valida la expresión, la evalúa y devuelve `{ result: <número> }` o un error.
4. **Salida al Usuario**  
   - El script recibe la respuesta JSON y muestra `resultDisplay.value = data.result`.

---

# Extensiones Futuras (Opcional)

| Idea | Descripción | Viabilidad |
|------|-------------|------------|
| **Soporte de funciones trigonométricas** | Añadir botones para `sin`, `cos`, `tan` y ampliar el parser del servidor. | Alta, requiere extensión del evaluador. |
| **Historial de cálculos** | Guardar cada operación en localStorage o base de datos y mostrar una lista desplegable. | Media, implica UI adicional y persistencia. |
| **Modo oscuro** | Añadir un toggle que cambie la paleta de colores usando CSS variables. | Baja, solo cambios front‑end. |
| **API de cálculo distribuida** | Desplegar el evaluador como microservicio independiente (por ejemplo en Docker). | Alta, mejora escalabilidad. |

---