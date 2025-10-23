# Non-Functional Requirements

- **Latency**
  - P95 redirect latency: 100 ms
  - P95 URL creation latency: 200 ms
  - _Note: P95 latency means that 95% of requests should complete within this time; 5% of requests may be slower._
- **Availability:** 99.99% uptime
- **Durability:** No loss of created URLs; replicated across multiple DB nodes
- **Throughput:** 
  - 2M URL creations/day
  - 20M redirects/day
  - Peak QPS: ~5k (estimate)
- **Scalability:** System can scale horizontally to handle 10× traffic (~50k QPS)
- **Consistency:** 
  - Strong consistency for URL creation (no collisions)
  - Eventual consistency acceptable for reads via caching
- **Security:** 
  - Optional rate-limiting to prevent abuse
  - Optional link privacy / access control
