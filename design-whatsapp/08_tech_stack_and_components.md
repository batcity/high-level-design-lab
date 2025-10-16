# Tech Stack and Components

This section outlines the recommended technologies for building a **WhatsApp-style real-time messaging platform** that can scale to hundreds of millions of users.  
The stack combines **relational + NoSQL databases**, **real-time messaging infrastructure**, and **global CDN-backed media delivery**.


## 🌐 API Gateway

**Chosen:** **Envoy**  

- High-performance L7 proxy; supports HTTP/2, gRPC, WebSockets.  
- Integrates with service meshes (Istio, Consul) for observability and resilience.  
- Handles **load balancing, rate limiting, authentication, and TLS termination**.  

**Alternatives:** Kong (rich plugins, easier setup), KrakenD (API aggregation).


## 💬 Core Services

All backend components are implemented as **stateless microservices**, deployed in containers and orchestrated via **Kubernetes**.  
We should use **different languages for different workloads** — services on the real-time data path prioritize concurrency and performance (Go), while metadata and orchestration services benefit from mature relational tooling (Java / Spring Boot).

---

### 🧩 Core Services Overview

| Service | Primary Language | Purpose |
|----------|------------------|----------|
| **Auth Service** | **Java (Spring Boot)** | Handles user authentication, session management, token issuance, and device association. Requires strong integration with relational metadata and external identity providers. |
| **User Service** | **Java (Spring Boot)** | Manages user profiles, contacts, account states, and preferences. Performs relational reads and writes in Spanner/MySQL. |
| **Conversation Service** | **Java (Spring Boot)** | Creates and manages 1:1 and group conversations, membership lists, and conversation metadata. Relies on transactional integrity and relational consistency. |
| **Message Service** | **Go** | Handles inbound and outbound message traffic. Connects to clients via WebSockets (or MQTT), publishes messages to Kafka, and fans them out to recipients. Optimized for extremely high concurrency and low latency. |
| **Message Persistence Service** | **Go** | Consumes message events from Kafka and writes them into Cassandra. Focuses on write throughput and efficient batching. |
| **Media Upload Service** | **Go** | Manages upload requests, generates pre-signed S3 URLs, and performs lightweight validation. Go’s concurrency model is ideal for IO-bound network operations. |

---

### 🧠 Language Rationale

| Language | Strengths | Ideal Workloads |
|-----------|------------|----------------|
| **Go** | Concurrency, low memory footprint, efficient networking | Real-time message handling, WebSocket servers, background stream processing |
| **Java (Spring Boot)** | Mature ecosystem, strong ORM support, configuration-driven | Business logic, relational data access, authentication and metadata management |

---

### 🧱 Summary by Layer

| Layer | Services | Language |
|--------|-----------|-----------|
| **Real-Time Path** | Message Service, Message Persistence Service, Media Upload Service | Go |
| **Metadata / Control Layer** | Auth Service, User Service, Conversation Service | Java (Spring Boot) |

---

This division keeps the **critical message path lightweight and performant** (Go) while maintaining **data integrity and strong consistency** in the metadata and control plane (Java).


## ⚡ Real-Time Communication Layer

**Chosen:** **WebSockets (or MQTT over WebSocket)**  

- Maintains persistent bidirectional connections with clients.  
- Enables instant delivery, typing indicators, read receipts, and presence updates.  
- Typically backed by a **connection manager cluster** that scales horizontally (e.g., using Redis pub/sub or Kafka for fanout).


## 📨 Message Queue

**Chosen:** **Apache Kafka**

- Handles asynchronous message delivery and persistence decoupling.  
- Ensures durability and ordering (partition by `conversation_id`).  
- Used for message ingestion, fanout, and event-driven updates (e.g., read receipts).  

**Alternatives:**  
- **Pulsar** → similar to Kafka but with built-in multi-tenancy and tiered storage.  
- **Redis Streams** → for lower-latency ephemeral message queues.


## 🧠 Databases

### 1. **Relational Store (Metadata)**
**Chosen:** **Google Spanner** (or MySQL / Postgres if self-managed)

Used for:
- Users, devices, groups, memberships, conversation metadata.  
- Strong consistency, relational integrity, transactional updates.

### 2. **Message Store**
**Chosen:** **Cassandra (or ScyllaDB)**

Used for:
- High-throughput, append-only message storage.  
- Messages partitioned by `conversation_id`, clustered by `timestamp`.  
- Tunable consistency and automatic TTL for old messages.

### 3. **Cache Layer**
**Chosen:** **Redis**

Used for:
- Presence and last-seen info.  
- Unread message counts and session state.  
- Fast lookups for frequently accessed metadata.


## 🗂️ Media & File Storage

| Component | Technology | Purpose |
|------------|-------------|----------|
| **Object Store** | AWS S3 (or GCS / MinIO) | Store encrypted media (photos, videos, documents). |
| **CDN** | Cloudflare / Akamai | Edge caching for global low-latency delivery. |
| **Access Control** | Pre-signed URLs | Time-limited, secure download links. |


## 🔐 Security & Encryption

- **End-to-End Encryption:** Signal protocol family (Curve25519, AES-GCM).  
- **Authentication:** OAuth2 + JWT (stateless access tokens, short TTL).  
- **Transport Security:** TLS for all client-server and inter-service traffic.  
- **Key Management:** HSM-based storage (e.g., AWS KMS, GCP KMS).  


## 🧩 Observability & Operations

| Category | Tools |
|-----------|-------|
| **Metrics** | Prometheus + Grafana |
| **Logging** | ELK or OpenSearch Stack |
| **Tracing** | OpenTelemetry + Jaeger |
| **Deployment** | Kubernetes (GKE/EKS/AKS) |
| **CI/CD** | GitHub Actions / ArgoCD |
| **Infra as Code** | Terraform |


## 🧱 Summary of Tech Stack

| Layer | Technology | Purpose |
|--------|-------------|----------|
| **API Gateway** | Envoy | Routing, rate-limiting, auth |
| **Backend Framework** | Spring Boot / Go | Core microservices |
| **Real-Time Transport** | WebSockets / MQTT | Live message delivery |
| **Queue / Stream** | Kafka | Async message flow & persistence decoupling |
| **Relational DB** | Spanner / MySQL | Metadata, relationships |
| **NoSQL Store** | Cassandra | Message persistence (append-only) |
| **Cache** | Redis | Presence, recent messages |
| **Object Storage** | S3 | Encrypted media |
| **CDN** | Cloudflare / Akamai | Global media delivery |
| **Observability** | Prometheus, Grafana, ELK | Monitoring & debugging |
| **Deployment** | Kubernetes + Terraform | Scalability & automation |


## 🧭 Design Rationale

- **Hybrid persistence** — relational (Spanner) for metadata, NoSQL (Cassandra) for high-throughput message writes.  
- **Asynchronous writes** — Kafka decouples user actions from durable storage.  
- **Real-time fanout** — WebSockets ensure instant delivery to connected users.  
- **Global performance** — CDN + regional clustering minimize latency.  
- **Resilience** — stateless services, replicated data stores, and message queues enable high availability.


📘 *This stack is designed for learning and reasoning about production-scale distributed messaging systems — not a literal WhatsApp implementation.*

## User Authentication Service, Message Persistence service and Media upload service:

I'd use a REST Service build using Spring boot (see Message service above for reasoning)

## Database:

I'd use something like Spanner for the Database considering the data model is highly relational, Spanner allows devs to scale horizontally pretty easily so it should be easy to scale it up to tens of millions of concurrent users

## CDN:

I'd use Akamai mostly since that's the only one i know lol

## Cloud storage:

S3 -> since this scale to store any amount of data

## Other:

I would use websockets to maintain a persistent connection between users who are online and the fan out web service that delivers messages to the users