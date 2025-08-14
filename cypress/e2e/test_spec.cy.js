cy.visit('/');
    
// Simulate button presses for '12+7'
cy.get('[data-cy="btn-1"]').click();
cy.get('[data-cy="btn-2"]').click();
cy.get('[data-cy="btn-plus"]').click();
cy.get('[data-cy="btn-7"]').click();

// Click equals
cy.get('[data-cy="btn-equal"]').click();

// Verify result displayed is '19'
cy.get('[data-cy="display"]').should('have.text', '19');