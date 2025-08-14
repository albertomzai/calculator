describe('Prueba E2E de la Calculadora', () => {
  it('debe calcular 12+7 y mostrar 19', () => {
    cy.visit('/');

    // Ingresar 12
    cy.contains('button', '1').click();
    cy.contains('button', '2').click();

    // Operador +
    cy.contains('button', '+').click();

    // Ingresar 7
    cy.contains('button', '7').click();

    // Igual y verificar resultado
    cy.contains('button', '=').click();
    cy.get('#display').should('contain.text', '19');
  });
} );