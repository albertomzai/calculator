describe('Calculator E2E', () => {
  it('Should calculate 5+3 correctly', () => {
    cy.visit('/')
    cy.get('[data-testid=btn-5]').click()
    cy.get('[data-testid=btn-plus]').click()
    cy.get('[data-testid=btn-3]').click()
    cy.get('[data-testid=btn-eq]').click()
    cy.get('#display').should('have.text', '8')
  })