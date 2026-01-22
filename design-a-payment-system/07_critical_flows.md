# Critical flows (Payment System):

This section documents the core end-to-end flows in a simple Payment system. It emphasizes handling duplicate transactions, webhooks used to notify the payment system about payment state changes on the provider side, payment reconciliation and other payment related failures

## 1. Payment flow:

| Step | Component                             | Action                                            |
| ---- | ------------------------------------- | ------------------------------------------------- |
| 1    | **User → Payment service** | User submits a payment using a unique identifier representing this payment
| 2    | **Payment Service -> records the payment in the DB**                      | Stores the unique reference to this payment in the DB, payment fails if this transaction has been attempted already |
| 3    | **Payment Service -> External payment provider**               | The payment service attempts the payment using the external payment provider and records the result
| 4 | **Payment Service -> returns the payment status to the user**     


## 2. Webhook flow for payment state changes from the external provider:

| Step | Component                             | Action                                            |
| ---- | ------------------------------------- | ------------------------------------------------- |
| 1    | **External Payment API → Payment service** | External Payment Provider sends a request to a designated webhook (API endpoint) on the payment service whenever there's updates from their side
| 2    | **Payment Service -> updates the payment in the DB**                      | Payment service updates the status of the payment in it's database |

## 3. Reconciliation flow:

**What is reconciliation and why do we need it:** 

**Payment reconciliation** is the process of periodically verifying that our internal payment records match the external payment provider’s source of truth.

In other words:

> “For every transaction we think happened, did the provider agree — and are we missing any updates?”

Reconciliation helps answer questions such as:
- Did we mark a payment as **pending** but the provider marked it **succeeded**?
- Did we **miss a webhook**?
- Did the provider **process a payment we never recorded**?
- Did the provider **retry or reverse** a transaction?


### Why Webhooks Are Not Enough

Webhooks are:
- ✅ Near-real-time
- ❌ Not guaranteed delivery
- ❌ Can arrive out of order
- ❌ Can fail due to downtime, deployments, or networking issues

Even the best payment providers explicitly state:

> “Webhooks are best effort, not guaranteed.”

Because of this, **reconciliation acts as a safety net**, ensuring our system eventually reaches the correct financial state even when webhooks fail or are missed.

**Flow steps:**


| Step | Component                   | Action                                                                     |
| ---- | --------------------------- | -------------------------------------------------------------------------- |
| 1    | Reconciliation Job          | Periodically scans transactions in non-final states (`pending`, `unknown`) |
| 2    | Job → External Provider API | Fetches authoritative status using `provider_txn_id`                       |
| 3    | Job → Payment Service DB    | Compares provider state with internal state                                |
| 4    | Job                         | Updates internal record if there’s a mismatch                              |
| 5    | Job                         | Emits alerts / logs for irreconcilable mismatches                          |
