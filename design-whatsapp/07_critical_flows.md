# ⚙️ Critical Flows (WhatsApp-Style Messaging)

This section documents the core end-to-end flows in a WhatsApp-like messaging system. It emphasizes **session-based authentication**, asynchronous persistence, real-time delivery, and offline handling.


## 🔑 0. User Login & Session Token Flow

**Goal:** Authenticate the user and issue a token for subsequent requests.  

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **User → Load Balancer → API Gateway** | User provides credentials (phone number + OTP, password, etc.). |
| 2 | **API Gateway → Auth Service** | Auth Service verifies credentials. |
| 3 | **Auth Service → API Gateway** | If valid, generates a **session token** (short-lived access token + optional long-lived refresh token). |
| 4 | **API Gateway → User** | Returns token to the client. Client stores token locally. |

**Key Considerations**  
- Tokens are signed and can be validated without database lookups.  
- Refresh tokens allow long-lived sessions without requiring full re-login.  
- Tokens are device-bound for security.

## 📨 1. Send Message (Text or Media Metadata)

**Goal:** Send messages using a session token without re-authenticating for each message.  

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **User → Load Balancer → API Gateway** | Sends message including **session token**. |
| 2 | **API Gateway → Token Validation** | Validates token signature and expiration (lightweight check, no full login). |
| 3 | **API Gateway → Message Service** | Forwards authenticated message payload to the Message Service. |
| 4 | **Message Service → Message Queue** | Publishes message event for asynchronous persistence and delivery. |
| 5 | **Message Queue → Message Persistence Service → Database** | Persists message to durable storage. |
| 6 | **Message Service → Receivers** | Fans out message to online recipients via socket connections. |
| 7 | **Receivers → Client** | Delivers message; sends delivery/read acknowledgment back. |

**Key Considerations**  
- Ensure message ordering and idempotency.  
- Token validation is fast and scalable.  
- Offline messages are queued for delivery when users reconnect.

## 🖼️ 2. Media Upload & Send Flow

**Goal:** Upload media to share in chats and send it as a message.

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **User → API Gateway → Media Upload Service** | User uploads media file; service validates file type/size and prepares storage. |
| 2 | **Media Upload Service → Cloud Storage (e.g., S3)** | Stores media for durability. |
| 3 | **Cloud Storage → CDN** | CDN caches media for fast retrieval. |
| 4 | **Media Upload Service → User** | Returns **media metadata** (URL, type, size, checksum) to the client. |
| 5 | **User → API Gateway → Message Service** | Client sends a “send message” request, including the **media metadata** instead of the file. |
| 6 | **Message Service → Message Queue → Persistence Service → Database** | Persists message payload (including media metadata) for durability. |
| 7 | **Message Service → Receivers** | Fans out message with media metadata to online recipients. |
| 8 | **Recipient Client → CDN** | Recipients fetch actual media from CDN using URL. |

**Key Considerations**  
- Media file is **only uploaded once**; message payload references metadata.  
- Enforce file validation and virus scanning during upload.  
- Use **signed URLs** for secure, time-limited access to media.  
- Handle partial uploads or retries gracefully.  
- Maintain message ordering and delivery acknowledgments for media messages.


## 🔁 3. Message Retrieval / Sync Flow

**Goal:** User fetches messages after logging in, reconnecting, or switching devices.

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **User → API Gateway → Message Service** | Client requests message history or missed messages through the API Gateway. |
| 2 | **Message Service → Database (Direct Query)** | Message Service queries the database directly to fetch messages and metadata since the last sync timestamp. |
| 3 | **Database → Message Service** | Database returns the relevant messages. |
| 4 | **Message Service → Client** | Messages are sent back synchronously to the client, often paginated. |
| 5 | **Client → CDN** | For messages containing media URLs, the client fetches actual media from the CDN. |

**Key Considerations**  
- Use pagination or cursors for efficient scrolling.  
- Track sync state (`last_synced_timestamp`) to fetch only new data.  
- Use read replicas or caching (e.g., Redis) for scalability.



## ⚡ 4. Real-Time Message Delivery Flow

**Goal:** Deliver messages instantly to online recipients.

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **Message Service → Receiver Device(s)** | Detects online recipients and pushes messages over open sockets (WebSocket/MQTT). |
| 2 | **Receiver Device** | Receives and displays the message in real time. |
| 3 | **Receiver Device → Message Service** | Sends delivery/read acknowledgment back to the server. |
| 4 | **Message Service → Persistence Service → Database** | Updates delivery/read status for durability and synchronization. |

**Key Considerations**  
- Optimize fan-out for group chats.  
- Handle reconnections and duplicate deliveries.  
- Monitor delivery latency (P99) and message queue lag.

---

## 🌙 5. Offline Message Handling

**Goal:** Ensure offline users receive pending messages upon reconnecting.  

| Step | Component | Description |
|------|-----------|-------------|
| 1 | **Message Queue** | Retains undelivered messages for offline users. |
| 2 | **User Reconnects → Message Service** | Identifies pending messages. |
| 3 | **Message Service → Client** | Delivers messages in correct order. |
| 4 | **Client → CDN** | Fetches media files if needed. |

**Key Considerations**  
- Guarantee message ordering after reconnection.  
- Limit backlog for long offline periods.  
- Update sync states and acknowledge delivery.

---

### 🧠 Summary

| Flow | Path Type | Key Services | Notes |
|------|-----------|--------------|-------|
| Login | Sync | Auth Service | Issues session tokens |
| Send Message | Async | Message Queue, Persistence Service | Durable writes, token-based auth |
| Media Upload | Async | Upload Service, Cloud Storage, CDN | Separate from messaging |
| Message Retrieval | Sync | Message Service → DB | Low-latency reads |
| Real-Time Delivery | Sync | Message Service, Receivers | Fast fan-out |
| Offline Handling | Hybrid | Message Queue, Message Service | Reliable catch-up delivery |

**Design Principle:**  
- Authenticate once per device; use token for subsequent requests.  
- Writes are decoupled and durable via the queue → persistence layer.  
- Reads are direct and optimized for latency.  
- Media served via CDN for performance and scalability.
