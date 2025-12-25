## Back-of-the-Envelope Calculations

Here's the **storage and traffic requirements** for a payment system:

### Storage estimates:

- **What are we storing?**
  - we're going to be storing all the transactions that occur with an idempotency key (ex: transaction_id) and their corresponding status
- Since there's going to be 200k transactions on average, we're going to be storing about 73,000,000 (73 million) transactions a year -> extrapolating that for 5 years - we're going to be storing 365 million records in our datastore
- **Storage requirement per transaction:** A production-ready payment record includes:
IDs (idempotency UUID ~36B), provider txn ID (VARCHAR ~40–64B),
amount/currency (DECIMAL ~8B, CHAR(3) ~3B),
timestamps (2 × TIMESTAMP ~16B),
status (TINYINT / ENUM ~1B),
nullable failure metadata (code/reason ~20–40B),
and database/index overhead (row header + PK/idempotency indexes ~60–90B).
Rule of thumb: ~200–250 bytes per transaction.
- **Total storage requirement for the next 5 years:**: 250 Bytes * 365 million = 91 GB which is fairly manageable for both MySQL/Postgres

### Traffic estimates:

we have the following transaction estimates from the assumptions:

- **Average transactions per day:** 200k
- **Average TPS (Transactions per second):** ~2.3 (200k / 24h / 3600)
- **Peak TPS (10× burst):** 20–30 TPS

Each transaction would perform the following queries

- write the transaction to the datastore with the idempotency key to ensure uniequeness
- If the write goes through, then attempt a payment transaction from sender to receiver -> but this query hits the external API
- get the status of the transaction and update the transaction
- **Note:** if the first write fails because a transaction exists already then we only return the status to the user - the first POC is not going to have retries

I'm going to assume that the External payments API is quite reliable - so a majority of the transactions would complete on the first try

This would mean that there would be 2 queries per transaction

so the traffic would be:

- **Average QPS:** 2 * 2.3 = 4.6
- **Peak QPS:** 2 * 30 = 60 QPS