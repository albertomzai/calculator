// cypress/e2e/calculator_spec.js
describe('Calculadora Web', () => {
  it('debe calcular 5 + 3 = 8', () => {
    cy.visit('/');
    cy.get('[data-testid=btn-5]').click();
    cy.get('[data-testid=btn-plus]').click();
    cy.get('[data-testid=btn-3]').click();
    cy.get('[data-testid=btn-equals]').click();
    cy.get('[data-testid=screen-result]').should('contain', '8');
  });
});