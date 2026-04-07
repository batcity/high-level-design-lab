# Tradeoffs and Alternatives

## Higher latency depending on user location:

- The current design does not account for a potentially global customer base, since the chosen mysql database or the service isn't deployed globally it could lead to high latency for users who are situated farther from these servers (For example: If the database and service is deployed in servers in India, customers from Canada might face high latency while accessing the payment service)


## Lower Reliability since the database isn't replicated

- The current design includes a single mysql DB that isn't replicated, this means that if the DB server goes down - then the service would be unusable. This could be resolved by creating read - write replicas, the tradeoff here is that it would introduce more complexity in the design

**NOTE:** The NFR mentions a replicated DB so revisit that document