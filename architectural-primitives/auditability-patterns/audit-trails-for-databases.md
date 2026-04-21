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

###  Log-based CDC (The "Standard")

CDC tools like Debezium treat the database logs as a commit stream. They connect to a source DB, tail the DB logs and streams them as events to your preferred destination (ex: a kafka topic)

**How it starts:** It reads from the Binary Log (MySQL), Write-Ahead Log (PostgreSQL), or Transaction Log (SQL Server).

**Pros:** Zero impact on database performance; captures every single change, including deletes.

**Cons:** It's bound by the log retention policy. If the log is gone, the history is gone.

Here's reference docs on How debezium handles change data capture while working with MySQL: https://debezium.io/documentation/reference/3.5/connectors/mysql.html

## 3. Event Sourcing

Event Sourcing is a pattern that shifts the source of truth from the current state of an object to a sequence of immutable events.

Here's how event sourcing works:

- App emits event first
- Event is persisted
- State is derived from events (so one needs a derived table in order to view the current state of the system for quick reads)

Below is a concrete breakdown of this flow using a banking scenario.


#### 1. App Emits Event
When a user performs an action, the application logic validates the request and emits an event. This is a statement of fact about something that has already happened.

* **Action:** User_A sends $20 to User_B.
* **Event Emitted:** `MoneyTransferred`
* **Payload:**
    ```json
    {
      "transactionId": "tx-987",
      "from": "User_A",
      "to": "User_B",
      "amount": 20.00,
      "timestamp": "2026-04-21T21:22:00Z"
    }
    ```

#### 2. Event is Persisted (The Event Store)
The event is appended to an "Event Store"—an append-only database. In this model, data is never updated or deleted. If a mistake is made, a new "Correction Event" is added instead.

**The Immutable Ledger:**

| Sequence | Event Type | Data |
| :--- | :--- | :--- |
| 1 | `AccountOpened` | `{"user": "User_A", "limit": 1000}` |
| 2 | `FundsDeposited` | `{"user": "User_A", "amount": 100}` |
| 3 | `MoneyTransferred` | `{"from": "User_A", "to": "User_B", "amount": 20}` |
| 4 | `MoneyTransferred` | `{"from": "User_A", "to": "User_C", "amount": 30}` |

#### 3. State is Derived (The Read Model)
The "Current Balance" is not stored in the Event Store. Instead, the state is derived by replaying the events. Since recalculating the balance from thousands of events for every query is inefficient, the system maintains a **Derived Table** specifically for high-speed reads.
#
### Maintaining the Derived Table
A "Projection" service listens to the event stream. Every time a `MoneyTransferred` event is persisted, the service immediately updates a standard relational table.

**Derived Table: `AccountBalances` (Optimized for Reads)**

| User ID | Current Balance | Last Event Processed |
| :--- | :--- | :--- |
| User_A | **$50.00** | Seq 4 |
| User_B | **$20.00** | Seq 3 |
| User_C | **$30.00** | Seq 4 |

#### Key Advantages
* **High Performance Reads:** Queries hit the Derived Table (e.g., `SELECT balance FROM AccountBalances WHERE userId = 'User_A'`), making reads nearly instantaneous.
* **Auditability:** The Event Store provides a 100% accurate history of how the $50 balance was reached ($0 + $100 - $20 - $30).
* **Reconstruction:** If the Derived Table is lost or corrupted, it can be completely rebuilt from scratch by replaying the Event Store from Sequence 1.

#### TODO: Key Disadvantages