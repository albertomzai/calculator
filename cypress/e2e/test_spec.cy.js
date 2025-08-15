describe('Prueba E2E de la Calculadora', () => {
  it('debe calcular 7+3 y mostrar 10', () => {
    cy.visit('/');

    // Ingresar 7
    cy.get('[data-testid="btn-7"]').click();

    // Operador +
    cy.get('[data-testid="btn-add"]').click();

    // Ingresar 3
    cy.get('[data-testid="btn-3"]').click();

    // Igual y verificar resultado
    cy.get('[data-testid="btn-equal"]').click();
    cy.get('[data-testid="display"]').should('contain.text', '10');
  });
});