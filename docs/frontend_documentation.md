# Visión General del Proyecto

Este proyecto es una **calculadora web sencilla** que permite a los usuarios realizar operaciones aritméticas básicas (suma, resta y división) directamente desde el navegador. La interfaz está construida con HTML5 y Bootstrap 5 para garantizar un diseño responsive y accesible. Cuando el usuario pulsa el botón “=”, la expresión se envía al servidor mediante una petición **POST** a `/api/calculate`. El backend procesa la expresión y devuelve el resultado, que luego se muestra en la pantalla de la calculadora.

El flujo es el siguiente:

1. El usuario introduce números y operadores mediante los botones.
2. La expresión se construye dinámicamente en el campo de texto `display`.
3. Al pulsar “=”, se envía la expresión al endpoint `/api/calculate` con formato JSON `{ expression: "..." }`.
4. El servidor evalúa la expresión, devuelve `{ result: <valor> }` o un mensaje de error.
5. La respuesta se muestra en el `display`; los errores aparecen como alertas Bootstrap.

El objetivo principal es demostrar una interacción cliente‑servidor ligera con JavaScript puro y una API REST minimalista.

---

# Arquitectura del Sistema

## Componentes principales

| Componente | Descripción |
|------------|-------------|
| **Cliente** | Navegador web que sirve `index.html`. Interfaz de usuario, lógica de construcción de la expresión y consumo de la API. |
| **Servidor** | Servicio REST expuesto en `/api/calculate`. Recibe expresiones, las evalúa y devuelve resultados o errores. |
| **Base de datos** | No se utiliza; todas las operaciones son in‑memory. |

## Diagrama Mermaid

```mermaid
graph LR
    A[Usuario] --> B[Cliente (index.html)]
    B --> C{Construcción de expresión}
    C --> D[Botones numéricos/operadores]
    D --> E[Campo display]
    E --> F[Evento “=”]
    F --> G[POST /api/calculate]
    G --> H[Servidor]
    H --> I[Evaluar expresión]
    I --> J{Resultado}
    J --> K[Respuesta JSON {result}]
    J --> L[Error JSON {error}]
    K --> M[Actualizar display]
    L --> N[Mostrar alerta]
```

---

# Endpoints de la API

| Método | Ruta | Parámetros | Respuesta | Código de estado |
|--------|------|------------|-----------|------------------|
| **POST** | `/api/calculate` | `application/json`: `{ "expression": "<string>" }` | `200 OK`: `{ "result": <number> }`<br>`400 Bad Request`: `{ "error": "<mensaje>" }` | 200, 400 |

## Ejemplo de solicitud

```http
POST /api/calculate HTTP/1.1
Content-Type: application/json

{ "expression": "12+7-5/2" }
```

## Ejemplo de respuesta exitosa

```json
{
  "result": 16.5
}
```

## Ejemplo de respuesta con error (expresión inválida)

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{ "error": "Expresión no válida" }
```

---

# Instrucciones de Instalación y Ejecución

> **Requisitos previos**  
> - Node.js v18+ (para el servidor)  
> - Navegador moderno (Chrome, Firefox, Edge)

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/usuario/calculadora-web.git
   cd calculadora-web
   ```

2. **Instalar dependencias del backend**  
   ```bash
   npm install express body-parser cors
   ```

3. **Crear archivo `server.js`** (si no existe) con el siguiente contenido:

   ```js
   const express = require('express');
   const bodyParser = require('body-parser');
   const cors = require('cors');

   const app = express();
   app.use(cors());
   app.use(bodyParser.json());

   // Servir archivos estáticos (index.html, etc.)
   app.use(express.static(__dirname));

   // API de cálculo
   app.post('/api/calculate', (req, res) => {
     const { expression } = req.body;
     try {
       // Evaluar expresión segura
       const result = eval(expression);
       if (typeof result !== 'number' || !isFinite(result)) throw new Error();
       res.json({ result });
     } catch (_) {
       res.status(400).json({ error: 'Expresión no válida' });
     }
   });

   const PORT = process.env.PORT || 3000;
   app.listen(PORT, () => console.log(`Servidor escuchando en http://localhost:${PORT}`));
   ```

4. **Iniciar el servidor**  
   ```bash
   node server.js
   ```

5. **Abrir la aplicación**  
   Navega a `http://localhost:3000` y comienza a usar la calculadora.

---

# Flujo de Datos Clave

1. **Entrada del usuario** → Botones numéricos/operadores → Función `appendToDisplay`.
2. **Construcción de expresión** → Campo de texto `display`.
3. **Evento “=”** → Llamada a `fetch('/api/calculate', ...)` con cuerpo `{ expression }`.
4. **Servidor** → Evalúa la expresión, devuelve JSON.
5. **Cliente** → Actualiza `display` o muestra alerta según respuesta.

---

# Extensiones Futuras

| Área | Posible mejora |
|------|----------------|
| **Seguridad** | Reemplazar `eval()` por un parser de expresiones (e.g., mathjs) para evitar ejecución arbitraria. |
| **Soporte de operaciones** | Añadir multiplicación, potencia y paréntesis. |
| **Persistencia** | Guardar historial de cálculos en localStorage o una base de datos ligera. |
| **Internacionalización** | Soportar múltiples idiomas mediante i18n. |
| **Pruebas** | Implementar pruebas unitarias tanto para el cliente (Jest + Testing Library) como para el servidor (Mocha/Chai). |

---