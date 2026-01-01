# Data model:

## 1. Entities:

- User
- Transactions

## 2. Relationships:

- Users create Transactions

## 3. ER Diagram

![alt text](payment-system-er-model.png)

## 4. Attributes 

**transactions table:**

| Attribute | Type | Notes |
|-----------|-----------|-----------|
| idempotency_key | BIGINT | unique identifier for each transaction (primary key) |
| status | varchar(16) | transaction status such as pending, processed etc |
| created_timestamp | TIMESTAMP |
| updated_timestamp | TIMESTAMP |