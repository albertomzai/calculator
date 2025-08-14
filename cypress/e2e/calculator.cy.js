describe('Prueba E2E de la Calculadora', () => {
  it('Debería calcular 12+7 y mostrar 19', () => {
    cy.visit('/');
    cy.contains('button', '1').click();
    cy.contains('button', '2').click();
    cy.contains('button', '+').click();
    cy.contains('button', '7').click();
    cy.contains('button', '=').click();
    cy.get('#display').should('contain.text', '19');
  });
});