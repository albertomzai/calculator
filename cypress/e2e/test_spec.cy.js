cy.visit('/');
  
// Enter 12
cy.contains('1').click();
cy.contains('2').click();

// Add +
cy.contains('+').click();

// Enter 7
cy.contains('7').click();

// Press equals
cy.contains('=').click();
  
// Verify result is 19
cy.get('.display, #display, .screen')
  .should('contain.text', '19');