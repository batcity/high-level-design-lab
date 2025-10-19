# Trade-offs and Alternatives

## Data Store: Cassandra vs Spanner for Message Storage

The main trade-off when choosing Cassandra versus Spanner for message storage comes down to **write performance and consistency**:

- **Spanner**: Achieves **strong global consistency** using consensus protocols across regions. This means messages are strictly ordered and consistent worldwide, but writes are **slower** due to cross-region coordination.  

- **Cassandra**: Achieves **local consensus within a region**, allowing messages to be **written and available immediately** in that region. Cross-region replication is **asynchronous**, so messages are **eventually consistent** globally.  

**Implications for chat systems:**

- Cassandra enables **low-latency message writes** and scales to millions of users, at the cost of potential temporary out-of-order delivery across regions.  
- Spanner ensures **strict global ordering**, but the increased latency can impact real-time chat responsiveness.

| Feature | Cassandra | Spanner |
|---------|-----------|---------|
| Write Latency | Low (local consensus) | Higher (global consensus) |
| Consistency | Eventual (cross-region) | Strong (global) |
| Ordering | Per-region; eventual globally | Strict globally |
| Best Use | High-throughput messages | Metadata or critical transactions |

> **Summary:** For high-volume, real-time messaging like WhatsApp, Cassandra-style stores are preferred because **low latency and availability are more important than perfect global ordering**.  