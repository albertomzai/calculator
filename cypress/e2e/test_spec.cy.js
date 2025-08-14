cy.visit('/');
cy.get('[data-testid="btn-1"]').click();
cy.get('[data-testid="btn-2"]').click();
cy.get('[data-testid="btn-plus"]').click();
cy.get('[data-testid="btn-7"]').click();
cy.get('[data-testid="btn-equal"]').click();
cy.get('[data-testid="display"]').should('have.text', '19');