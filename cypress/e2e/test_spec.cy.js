describe('Prueba E2E de la Calculadora', () => {
  const baseUrl = 'http://localhost:5000/frontend/index.html';

  beforeEach(() => {
    cy.visit(baseUrl);
  });

  it('debe calcular 12+7*3 y mostrar 33', () => {
    // Ingresar 1,2
    cy.get('[data-testid="btn-1"]').click();
    cy.get('[data-testid="btn-2"]').click();

    // Operador +
    cy.get('[data-testid="btn-plus"]').click();

    // Ingresar 7
    cy.get('[data-testid="btn-7"]').click();

    // Operador *
    cy.get('[data-testid="btn-multiply"]').click();

    // Ingresar 3
    cy.get('[data-testid="btn-3"]').click();

    // Igual y verificar resultado
    cy.get('[data-testid="btn-equal"]').click();
    cy.get('[data-testid="display-result"]').should('contain.text', '33');
  });

  it('debe limpiar la expresión y el resultado al pulsar Clear', () => {
    // Ingresar 5,6
    cy.get('[data-testid="btn-5"]').click();
    cy.get('[data-testid="btn-6"]').click();

    // Operador -
    cy.get('[data-testid="btn-minus"]').click();

    // Igual para generar resultado
    cy.get('[data-testid="btn-equal"]').click();
    cy.get('[data-testid="display-result"]').should('not.be.empty');

    // Pulsar Clear
    cy.get('[data-testid="btn-clear"]').click();

    // Verificar que pantalla y resultado están vacíos
    cy.get('[data-testid="display-expression"]').should('have.text', '');
    cy.get('[data-testid="display-result"]').should('have.text', '');
  });

  it('debe mostrar un mensaje de error al enviar una expresión inválida', () => {
    // Pulsar igual sin ingresar nada
    cy.get('[data-testid="btn-equal"]').click();

    // Verificar que aparece el mensaje de error
    cy.get('[data-testid="error-message"]')
      .should('be.visible')
      .and('contain.text', 'Error');
  });
});