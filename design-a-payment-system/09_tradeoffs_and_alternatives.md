# Tradeoffs and Alternatives

## Higher latency depending on user location:

The current design does not account for a potentially global customer base, since the chosen mysql database or the service isn't deployed globally it could lead to high latency for users who are situated farther from these servers (For example: If the database and service is deployed in servers in India, customers from Canada might face high latency while accessing the payment service)

The database needs to be highly consistent since this is a payment system and there's very little room for error, so we're accepting the tradeoff that latency would be higher for users that are farther from the DB

> Note: A potential improvement would be to tie users/payers to specific regions, and then route their reads and writes to databases in their "home region", this would still deliver strong consistency, while reducing latency