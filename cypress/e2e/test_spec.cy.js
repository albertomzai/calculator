describe('Prueba E2E de la Calculadora', () => {
  it('debe calcular 7+3 y mostrar 10', () => {
    cy.visit('/');
    
    // Ingresar 7
    cy.get('[data-testid="num-7"]').click();
    
    // Operador +
    cy.get('[data-testid="op-add"]').click();
    
    // Ingresar 3
    cy.get('[data-testid="num-3"]').click();
    
    // Igual y verificar resultado
    cy.get('[data-testid="equal"]').click();
    
    // Esperamos que la pantalla muestre el resultado 10
    cy.get('[data-testid="display"]').should('contain.text', '10');
  });
});