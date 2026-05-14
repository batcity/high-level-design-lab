# Tradeoffs and alternatives:

# How to Think About Trade-offs & Alternatives

Trade-offs are easier to identify when thinking in terms of **system pressures** rather than technologies.

Every architecture decision optimizes for something while sacrificing something else.

Examples of common pressures:

- Latency
- Scalability
- Consistency
- Availability
- Cost
- Operational simplicity
- Developer velocity
- Flexibility

A useful way to discover trade-offs is to repeatedly ask:

1. What problem does this choice solve?
2. What new problem does this choice create?
3. What simpler alternative exists?
4. Why wasn’t the simpler option enough?
5. What does this system optimize for?
6. When would this design stop working?

Examples:

| Choice | Optimizes For | Trade-off |
|---|---|---|
| Redis cache | Low latency | Stale data / cache invalidation |
| Kafka | Throughput & decoupling | Operational complexity |
| Cassandra | High write scalability | Eventual consistency |
| Global DB | Strong consistency | Higher latency |
| Microservices | Independent scaling | Distributed system complexity |

A good trade-offs section should explain:

- Why a design was chosen
- What constraints influenced the decision
- What downsides were knowingly accepted
- What alternatives were considered
- Under what future conditions the decision should be revisited

A helpful mindset:

> “What pain is this design avoiding, and what pain is it accepting instead?”