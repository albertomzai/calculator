{
  "files": [
    {
      "filename": "cypress/e2e/calculator.cy.js",
      "action": "create_or_update",
      "code": [
        "describe('Prueba E2E de la Calculadora', () => {",
        "  it('Debería calcular 12+7 y mostrar 19 en la pantalla', () => {",
        "    // 1. Visitar la página principal",
        "    cy.visit('/');",
        "",
        "    // 2. Simular pulsaciones de botones para la expresión '12+7'",
        "    cy.contains('button', '1').click();",
        "    cy.contains('button', '2').click();",
        "    cy.contains('button', '+').click();",
        "    cy.contains('button', '7').click();",
        "",
        "    // 3. Hacer clic en el botón de igual (=)",
        "    cy.contains('button', '=').click();",
        "",
        "    // 4. Verificar que la pantalla muestra el resultado correcto ('19')",
        "    cy.get('#display').should('contain.text', '19');",
        "  });",
        "});"
      ]
    }
  ]
}