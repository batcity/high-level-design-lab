# Non Functional Requirements:

- **Latency:**

    - Internal processing latency (P95):
    ≤ 50 ms excluding external payment provider calls
    - End-to-end API latency (P95):
    ≤ 2–3 seconds for synchronous payment confirmation
    - Timeouts:
    External payment API calls time out after a bounded threshold (e.g., 3–5s)

- **Availability:** Uptime should be 99.99% (API availability; not payment success)

- **Throughput:**
    - **Average transactions per day:** 200k
    - **Peak QPS:** 2 * 30 = 60 QPS based on the peak transactions per second

- **Scalability:** The system should be able to serve 10x Peak load which roughly translates to 600 QPS

- **Durability:** No loss of Transaction data, they should be replicated across multiple DB nodes to avoid data loss

- **Consistency:** Strong Consistency for Transaction data

- **Security:** 

    - Transport security: TLS for all inbound and outbound traffic
    - No storage of raw card data
        - **Use provider-side tokenization:** Card details are sent directly to the payment provider, which returns a non-sensitive token; our system stores and uses only the token, never the raw card data.