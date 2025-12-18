# Problem framing:

Design a payment system that transfers money from a payer’s credit or debit card to a payee’s bank account using an external payment API.

## In-scope features / Functional Requirements

1. **Accept Payment Request**
   - Credit or debit card details
   - Payment amount
   - Payee bank account details

2. **Process Payment**
   - Use an external payment provider API to:
     - Charge the card
     - Transfer the funds to the specified bank account

3. **Return Payment Status**
   - Success
   - Failure


## Out of Scope

- User accounts or profiles
- Wallets or stored balances
- Saved cards or bank accounts
- Merchant onboarding and management
- Refunds, chargebacks, and disputes
- Currency conversion