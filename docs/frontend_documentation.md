# Visión General del Proyecto

El proyecto es una **calculadora web** de una sola página que permite al usuario introducir expresiones matemáticas y obtener el resultado. La lógica de cálculo se delega en un backend Flask, manteniendo la interfaz ligera y sin dependencias externas.

La aplicación consta de:

- Un único archivo `index.html` con HTML, CSS (Grid) y JavaScript ES6.
- Botones para números, operadores, punto decimal, igual (`=`), y borrar (`C`).
- Una pantalla que muestra la expresión en construcción y el resultado final.

El flujo de interacción es sencillo: al pulsar los botones se construye una cadena `expression`. Al pulsar `=`, esa cadena se envía al endpoint `/api/calculate` mediante `fetch`. La respuesta JSON contiene el valor calculado, que reemplaza la expresión mostrada.

---

# Arquitectura del Sistema (Frontend)

```mermaid
graph TD;
A[Usuario] -->|Interacción| B[Botones]
B -->|Construye| C{Expresión}
C -->|Envía| D[/api/calculate (Backend)]
D -->|Resultado JSON| E[JavaScript]
E -->|Actualiza| F[Display]
```

**Componentes clave**:

- **HTML**: estructura semántica con `div.calculator`, `div.display` y `div.buttons`. Cada botón tiene un atributo `data-value` que indica su valor.
- **CSS**: diseño responsivo mediante Grid. Colores contrastantes para operadores, igual, y borrar.
- **JavaScript**:
  - `expression`: cadena mutable que representa la entrada del usuario.
  - `updateDisplay()`: actualiza el contenido de `#display`.
  - Event listeners:
    - Botones con `data-value`: añaden su valor a `expression` salvo operadores en posición inicial.
    - Botón `C`: resetea la expresión.
    - Botón `=`: llama a `calculate()` que envía una solicitud POST al backend y muestra el resultado.

---

# Endpoints de la API

| Método | Ruta | Descripción | Cuerpo | Respuesta |
|--------|------|-------------|--------|-----------|
| **POST** | `/api/calculate` | Evalúa una expresión matemática segura. | `{ "expression": "5*8-3" }` | `{ "result": 37 }` |

El endpoint es implementado en Flask con la función `safe_eval` (no incluida aquí) que garantiza que solo se evalúan operadores aritméticos básicos.

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/albertomzai/calculator.git
   cd calculator
   ```

2. **Instalar dependencias (backend)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install flask
   ```

3. **Ejecutar el servidor Flask**:

   ```bash
   export FLASK_APP=app.py  # o el nombre del archivo que contiene la app
   flask run --port 5000
   ```

4. **Abrir el frontend**:

   - Si el servidor Flask sirve archivos estáticos, navega a `http://localhost:5000/index.html`.
   - O bien abre directamente `index.html` en tu navegador.

---

# Flujo de Datos Clave

- **Entrada del usuario** → Botones (`data-value`) → Construcción de cadena `expression`.
- **Solicitud HTTP** (`fetch('/api/calculate')`) con cuerpo JSON `{ expression }`.
- **Backend** procesa la expresión y devuelve `{ result }`.
- **JavaScript** actualiza el DOM con el resultado.

---

# Extensiones Futuras (Opcional)

1. **Soporte de funciones trigonométricas**: añadir botones para `sin`, `cos`, etc., y extender la lógica del backend con un evaluador seguro que incluya `math.sin`.

2. **Persistencia de historial**: guardar expresiones y resultados en localStorage o en una base de datos ligera (SQLite) para permitir al usuario revisar cálculos anteriores.

3. **Modo oscuro/ligth toggle**: añadir un botón que cambie la paleta de colores mediante clases CSS dinámicas.

4. **Validación avanzada del frontend**: impedir entradas inválidas antes de enviar a la API (por ejemplo, operadores consecutivos).
