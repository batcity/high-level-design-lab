# Tradeoffs and alternatives:

## API Gateway

**Current choice:** kong

### **What problem does this choice solve:** 

This choice was made to solve two problems

1. There are multiple services that are part of the solution, the gateway needs to intelligently route user requests to the correct service based on the incoming request type

2. To distribute traffic across different servers in order to handle a large number of users, the additional benefit here is reliability since having a single web server would introduce a single point of failure

So it addresses two major system pressures

- Reliability
- Throughput / Traffic


### **What new problem does this choice create:**

I've substituted one single point of failure for another here, if the API gateway is down then the entire service would be down

I've also introduced additional complexity since devs would need to maintain the API gateway

### **What simpler alternative exists?**

Using a standard Layer 4/7 Load Balancer (e.g., AWS ALB or Nginx) and letting the frontend application handle the routing by talking directly to different public service endpoints.

### **Why wasn’t the simpler option enough?**

Decoupling: Keeps backend microservice architecture hidden. Frontend only needs to know one base URL.

Centralized Security: Kong handles JWT validation at the edge. Inner services don't waste resources processing unauthorized requests or duplicating auth logic.

Attack Surface: Keeps microservices securely isolated in a private network rather than exposing multiple public-facing endpoints.

### **What's the tradeoff here:**

**Pros:**

- Increased security
- Decoupling
- Ability to tolerate heavy traffic

**Cons & Mitigations:**

* **Single Point of Failure:** If the gateway goes down, everything goes down. 
  * *Mitigation:* Deploy Kong in a stateless cluster (multiple nodes) behind an automated cloud provider load balancer.
* **Increased Technical Complexity:** Teams must configure and maintain the gateway.
  * *Mitigation:* Use Kong’s declarative (DB-less) configuration format integrated into the CI/CD pipeline to treat infrastructure as code.


## URL shortener service, User Authenticaton Service

**Current choice:** Go (Golang) + Gin Framework

### **What problem does this choice solve:**

This combination was chosen to solve several critical scaling pressures for a system handling 10M MAU and a 5,000 peak QPS:

High Concurrency & Low Latency: Go’s native concurrency model utilizes "Goroutines" instead of heavy OS threads. Goroutines require only 2 KB of initial memory compared to Java’s 1 MB per thread, allowing a single application node to process tens of thousands of concurrent redirect requests effortlessly.

Minimal Infrastructure Costs: Go compiles directly to a single, bare-metal machine-code binary. It completely bypasses the massive CPU/RAM overhead of a virtual machine layer (like the JVM), allowing the system to scale horizontally on incredibly small, cost-effective container footprints.

Blazing Fast HTTP Routing: The Gin framework uses a custom version of Radix Tree routing, which dramatically optimizes URL path parsing and speeds up the core redirection lookup flow.

### **What new problem does this choice create:**

Lack of Built-In Enterprise Tooling: Unlike Spring Boot, Go does not provide a "batteries-included" ecosystem for security and object-relational mapping (ORM). Features like password hashing, token generation, and complex database migrations require pulling in separate, standalone libraries.

Explicit Error Handling: Go forces developers to explicitly handle every single error in code (if err != nil), which increases code verbosity and can slow down initial feature implementation.

### **What simpler alternative exists?**

Using Python + FastAPI. Python allows for incredibly fast development cycles, has minimal boilerplate, and offers an easy learning curve for engineers.

### **Why wasn’t the simpler option enough?**

The Global Interpreter Lock (GIL): Python is inherently single-threaded. To utilize a multi-core CPU under our estimated 5,000 peak QPS, Python requires spawning multiple parallel worker processes, which multiplies its memory consumption and caps raw execution throughput.

Predictable Latency Profiles: Python handles async I/O well, but under high concurrent loads, its execution speed and memory recycling can cause unpredictable latency spikes, threatening our target P95 redirect latency of 100 ms.

### **What's the tradeoff here:**

**Pros:**

Ultra-Low Memory Footprint: Idle Go containers hover around less than 10MB of RAM, compared to Spring Boot's typical 50+ MB requirement.

Instantaneous Boot Times: Go binaries boot in milliseconds, allowing Kubernetes HPA (Horizontal Pod Autoscaler) to respond to sudden traffic spikes instantly.

Consistent Latency: Go’s concurrent garbage collector operates with sub-millisecond pauses, ensuring a flat, predictable latency curve for users hitting short link redirects.

**Cons & Mitigations:**

Manual Security / Auth Implementation: Go has no direct equivalent to a massive framework like Spring Security.

Mitigation: Because our API Gateway (Kong) handles JWT verification at the edge, the inner Go URL Service only needs to read a plain-text header injected by the gateway (X-User-Id), bypassing the need for a complex inner authentication framework. For token generation in the Auth service, standard libraries like golang-jwt/jwt and crypto/bcrypt can be easily implemented with minimal middleware.

Strict Ecosystem Shift: Developers transitioning from object-oriented languages must learn Go’s structural typing and explicit error handling models.

Mitigation: Establish strict coding standards and utilize Gin’s robust middleware community to standardize logging, recovery, and request validation.

### **Additional Evidence:**
https://github.com/batcity/go-gin-vs-java-spring-boot-memory-comparison

## Cache

current choice: Redis

### **What problem does this choice solve:**

This choice solves the latency problem when users query the URL shortener service, reading from the DB is a much slower process since it's typically on permanent storage like an SSD. Loading up the data in an in memory db like REDIS in addition to the permanent storage would make queries much faster

### **What new problems does this choice create:**

It creates the following problems:

- we're going to have to maintain a redis server in addition to the existing database
- we're going to have to come up with a cache eviction strategy since the in memory db might not be able to hold all the data we need

### **What simpler alternative exists?**

Perhaps using an AWS managed key value store like Dynamodb that has both permanent storage and an in memory cache built on top would make things a bit simpler

### **Why wasn’t the simpler option enough?**

Actually I'm not sure here, I think the simpler option might be the better one, although I haven't reviewed the cost structure for dynamodb

### **What's the tradeoff here:**

Tradeoff ofcourse is additional complexity for lower latency

**Pros:**

- Lower latency for queries

**Cons & Mitigations:**

- Higher complexity

**TODO:**

# Take a look at these recommendations from gemini

Across the URL shortener files (`08_tech_stack_and_components.md`, `09_WIP_tradeoffs_and_alternatives.md`, `07_critical_flows.md`, and the architecture diagram), the cache section has a solid foundation, but there are several critical design gaps, contradictory notes, and missed opportunities.

---

### 1. Strengths in the Current Design

* **Sensible Tool Choice:** Selecting Redis over Memcached for click-tracking atomic increments (`INCR`) and analytics sets (`Sorted Sets`) is a standard, production-ready justification.
* **Separation of Concerns:** The cache isolates the read-heavy redirect path (estimated at 10:1 to 20:1 reads vs. writes) from the relational database.

---

### 2. Disconnects & Contradictions

* **Cache Missing from Critical Flows:**
* In `07_critical_flows.md` under **Step 2 (Redirect User)**:
> *"Looks up the short code (`xyz`) in the data store to retrieve the original long URL."*


* It mentions the generic "data store" and does not specify **Cache-Aside (read-through)** semantics (check Redis first, fallback to MySQL on miss, hydrate cache).


* **Diagram Flow Ambiguity:**
* In `URL-shortener-system-design.excalidraw`, the arrow leads from `URL shortener Service` to `Cache`, and then from `Cache` directly to `Database`.
* In application-level caching (Redis), the application service typically queries Redis; if it misses, the **application** reads MySQL and populates Redis. Redis does not natively act as an intermediary forwarder to MySQL unless an active cache/read-through proxy layer is implemented.


* **DynamoDB Comparison in Tradeoffs:**
* In `09_WIP_tradeoffs_and_alternatives.md`, under simpler alternatives, you wrote:
> *"Perhaps using an AWS managed key value store like Dynamodb that has both permanent storage and an in memory cache built on top... Actually I'm not sure here, I think the simpler option might be the better one..."*


* **The reality:** DynamoDB + DAX (DynamoDB Accelerator) is indeed a fully managed NoSQL alternative, but DAX is expensive, provisioned, and adds VPC routing complexity. More importantly, using Redis + MySQL retains relational access for user dashboards (`user_id` foreign keys, joins, and pagination), which DynamoDB makes clunkier without carefully planned Global Secondary Indexes (GSIs).



---

### 3. Critical Sizing & Strategy Gaps

#### Eviction Strategy & Capacity

* **Policy:** You mentioned needing an eviction strategy in the tradeoffs file, but haven't chosen one. **LRU (Least Recently Used) / `allkeys-lru**` is the gold standard here because URL popularity follows a steep 80/20 Pareto distribution (most clicks hit recent or viral links).
* **RAM Sizing (The 80/20 Rule):**
* Traffic assumptions state 20M redirects/day.
* 20% of active daily links generate 80% of redirect traffic: $20\text{M} \times 0.20 = 4\text{M}$ URLs/day.
* Memory per cache entry (key + value + metadata overhead): $\approx 250$ bytes.
* Daily working set memory: $4\text{M} \times 250\text{ bytes} \approx 1\text{ GB}$.
* With a conservative 2-day hot cache + Redis overhead, an **8 GB to 16 GB Redis cluster** easily caches virtually all active redirect traffic.



#### Missing Cache Failure & Concurrency Protections

* **Cache Stampede (Thundering Herd):** If a viral link expires or gets evicted and thousands of concurrent requests miss simultaneously, they will all hammer the MySQL follower replica. **Solution:** Distributed locking (e.g., Redis mutex) or single-flight/probabilistic early expiration (XFetch).
* **Cache Penetration (Lookup of Non-Existent Keys):** If malicious actors generate millions of random nonexistent short URLs, every request bypasses Redis and hits the database. **Solution:** Store empty/null values with a short TTL (e.g., 2–5 minutes) or place a **Bloom filter** at the API Gateway/Service layer.
* **Write Pattern:** Specify whether you want:
* **Cache-Aside:** Simple, reads populate the cache, but initial read incurs DB latency.
* **Write-Through / Write-Around:** If writes are cached immediately upon link creation, read latency on first click drops to sub-millisecond levels.



---

### Recommended Updates to `09_WIP_tradeoffs_and_alternatives.md`

Replace the placeholder/uncertain text in your cache tradeoffs section with:

```markdown
## Cache

**Current choice:** Redis (Cluster mode, with replication)

### What problem does this choice solve:
Drastically cuts redirect latency (P95 target < 100 ms) by serving ~80-90% of redirection requests directly from RAM instead of persistent disk storage (MySQL). It also provides native atomic data structures (`INCR`, `ZSET`) for real-time link access metrics.

### What new problem does this choice create:
- Memory management & cache eviction overhead.
- Dual-source consistency (stale URLs if links can be updated/deleted).
- Risk of cache stampede or penetration under high load.

### What simpler alternative exists?
- Memcached (pure key-value, multi-threaded).
- DynamoDB with DAX (fully managed integrated database + cache).

### Why wasn’t the simpler option enough?
- Memcached lacks native atomic increments and complex data structures needed for analytics without external distributed locks.
- DynamoDB + DAX eliminates MySQL maintenance, but makes relational user dashboards (e.g., paginating/sorting user links by creation date) more rigid and expensive to query compared to indexed MySQL queries.

### What's the tradeoff here:
Accepting operational complexity (managing Redis replication, failovers, and cache coherency) in exchange for single-digit millisecond redirect latency and flexible analytics data structures.

**Pros:**
- Ultra-low latency lookups (sub-5 ms).
- Reduces MySQL read traffic from 5,000 peak QPS to low hundreds.

**Cons & Mitigations:**
- **Cache Eviction / OOM:** Configure maxmemory policy to `allkeys-lru` with a standard 8–16 GB memory footprint based on the 80/20 traffic rule.
- **Cache Penetration:** Cache null/empty entries with a short TTL (60s) or front with a Bloom filter.
- **Cache Stampede:** Use singleflight request deduplication on the URL shortener application nodes.

```

## Database:

current choice: Mysql with replication

### **What problem does this choice solve:**
### **What new problem does this choice create:**
### **What simpler alternative exists?**
### **Why wasn’t the simpler option enough?**
### **What's the tradeoff here:**

**Pros:**
**Cons & Mitigations:**
