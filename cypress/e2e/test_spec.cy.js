describe('Prueba E2E de la Calculadora', () => {
  it('debe calcular 12+7 y mostrar 19', () => {
    cy.visit('/');

    // Ingresar 1 y 2
    cy.get('[data-testid="btn-1"]').click();
    cy.get('[data-testid="btn-2"]').click();

    // Operador +
    cy.get('[data-testid="btn-plus"]').click();

    // Ingresar 7
    cy.get('[data-testid="btn-7"]').click();

    // Igual y verificar resultado
    cy.get('[data-testid="btn-equals"]').click();
    cy.get('[data-testid="calculator-display"]')
      .should('contain.text', '19');
  });

  it('debe calcular 5*8-3 y mostrar 37', () => {
    cy.visit('/');

    // Ingresar 5
    cy.get('[data-testid="btn-5"]').click();

    // Operador *
    cy.get('[data-testid="btn-multiply"]').click();

    // Ingresar 8
    cy.get('[data-testid="btn-8"]').click();

    // Operador -
    cy.get('[data-testid="btn-minus"]').click();

    // Ingresar 3
    cy.get('[data-testid="btn-3"]').click();

    // Igual y verificar resultado
    cy.get('[data-testid="btn-equals"]').click();
    cy.get('[data-testid="calculator-display"]')
      .should('contain.text', '37');
  });

  it('debe mostrar error al enviar expresión inválida', () => {
    cy.visit('/');

    // Ingresar 8 y operador sin número después
    cy.get('[data-testid="btn-8"]').click();
    cy.get('[data-testid="btn-plus"]').click();

    // Igual y verificar que aparece mensaje de error
    cy.get('[data-testid="btn-equals"]').click();
    cy.get('[data-testid="calculator-display"]')
      .should('contain.text', 'Error');
  });
});