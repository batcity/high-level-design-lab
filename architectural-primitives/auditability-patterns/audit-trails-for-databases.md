# Audit trail for Databases:
## TODO: Refine this document

Several systems like payment systems for example would need to maintain an Audit trail (For things like regulatory compliance, Fraud detection and prevention etc). Considering this, the question is what is a good architectural pattern to maintain an audit trail for databases (this must be DB agnostic)

> No single pattern fully satisfies audit requirements. A robust audit architecture typically combines application-level event generation for semantic richness with database-level CDC for completeness and verification.

## 1. Asynchronous Event-Driven Auditing

This pattern relies on capturing state changes at the application or service level and publishing them as events to a dedicated logging infrastructure.

**How it Works:**   
The Interceptor: An interceptor or middleware within the application layer catches "Write" operations (Create, Update, Delete) before or after they hit the database.

**Event Generation:** The system constructs an Audit Event Object containing:

```
Who: User ID or Service ID.  
What: The specific action (e.g., PAYMENT_AUTHORIZED).  
When: Timestamp (ISO 8601).  
Where: Source IP, Metadata, or Service Name.  
Data: The "Before" and "After" snapshots (payload).
```

**Message Broker:** The event is sent to a message broker (like Apache Kafka or RabbitMQ). This decouples the audit process from the main transaction; if the audit system is slow, the payment processing isn't delayed.

**Audit Consumer:** A dedicated service consumes these events and writes them to a WORM (Write Once, Read Many) storage, such as an immutable S3 bucket or a specialized Ledger Database.

## 2. CDC - Change Data Capture

## 3. Event Sourcing
