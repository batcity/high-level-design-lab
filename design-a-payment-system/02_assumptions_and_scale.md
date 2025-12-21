# Assumptions and scale:

The following assumptions provide baseline inputs for sizing and architecture decisions. They describe expected usage patterns and system inputs.

- **Users:** 2 million MAU, 200k Daily active users
- **Transactions per active user:** 0.5–1.5 / day (average ~1)
- **Peak concurrency:** 20k–50k during business hours / sale events
- **Average transactions per day:** 200k
- **Average TPS (Transactions per second):** ~2.3 (200k / 24h / 3600)
- **Peak TPS (10× burst):** 20–30 TPS
- **Read/Write distribution:**
    - On the payment request path, reads and writes are evenly distributed (one idempotency read and one transactional write per request).
    - Additional reads/writes from:
        - Webhook processing
        - Retry handling
        - Reconciliation jobs
