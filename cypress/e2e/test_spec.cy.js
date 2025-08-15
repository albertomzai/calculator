describe('Prueba E2E de la Calculadora', () => {
  it('debe calcular 7+3 y mostrar 10', () => {
    // Visitar la página principal
    cy.visit('/');

    // Ingresar el número 7
    cy.get('[data-testid="button-7"]').click();

    // Operador +
    cy.get('[data-testid="button-plus"]').click();

    // Ingresar el número 3
    cy.get('[data-testid="button-3"]').click();

    // Igual y verificar resultado
    cy.get('[data-testid="button-equal"]').click();
    cy.get('[data-testid="display"]').should('contain.text', '10');
  });
});