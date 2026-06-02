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

**Current choice:** Java + Spring boot

### **What problem does this choice solve:**

This combination was chosen to solve the following problems:

- To reduce boilerplate: Spring boot offers a bunch of built in features that would remove the need to custom build several features that are commonly used in web services

### **What new problem does this choice create:**

- The problem now is that Devs would need to be familiar with both Java and the Spring boot framework in order to be productive
- Spring boot is highly opinionated and it might prevent certain things that the Devs might want to do

### **What simpler alternative exists?**

Using Java alone would probably make dev work more complex, Using something like Python + FastAPI might be a simpler alternative since Python is famous for allowing fast Dev cycles


### **Why wasn’t the simpler option enough?**

I'm actually not completely sure, I keep reading that Java + Spring boot is what most enterprises choose and I don't know if Python + FastAPI or another backend engine might be better


### **What's the tradeoff here:**

**Pros:**
**Cons & Mitigations:**

### Actually gemini recommends this, take a look at this to see if it's true

### Verify this, check what an idle spring boot docker container uses in terms of memory and do the same thing for go

I've verified that difference in memory usage, here's the comparison: https://github.com/batcity/go-gin-vs-java-spring-boot-memory-comparison

URL Shortener Service & User Authentication Service
Current choice: Go (Golang) + Gin Framework

What problem does this choice solve:
This combination was chosen to solve several critical scaling pressures for a system handling 10M MAU and a 5,000 peak QPS:

High Concurrency & Low Latency: Go’s native concurrency model utilizes "Goroutines" instead of heavy OS threads. Goroutines require only 2 KB of initial memory compared to Java’s 1 MB per thread, allowing a single application node to process tens of thousands of concurrent redirect requests effortlessly.

Minimal Infrastructure Costs: Go compiles directly to a single, bare-metal machine-code binary. It completely bypasses the massive CPU/RAM overhead of a virtual machine layer (like the JVM), allowing the system to scale horizontally on incredibly small, cost-effective container footprints.

Blazing Fast HTTP Routing: The Gin framework uses a custom version of Radix Tree routing, which dramatically optimizes URL path parsing and speeds up the core redirection lookup flow.

What new problem does this choice create:
Lack of Built-In Enterprise Tooling: Unlike Spring Boot, Go does not provide a "batteries-included" ecosystem for security and object-relational mapping (ORM). Features like password hashing, token generation, and complex database migrations require pulling in separate, standalone libraries.

Explicit Error Handling: Go forces developers to explicitly handle every single error in code (if err != nil), which increases code verbosity and can slow down initial feature implementation.

What simpler alternative exists?
Using Python + FastAPI. Python allows for incredibly fast development cycles, has minimal boilerplate, and offers an easy learning curve for engineers.

Why wasn’t the simpler option enough?
The Global Interpreter Lock (GIL): Python is inherently single-threaded. To utilize a multi-core CPU under our estimated 5,000 peak QPS, Python requires spawning multiple parallel worker processes, which multiplies its memory consumption and caps raw execution throughput.

Predictable Latency Profiles: Python handles async I/O well, but under high concurrent loads, its execution speed and memory recycling can cause unpredictable latency spikes, threatening our target P95 redirect latency of 100 ms.

What's the tradeoff here:
Pros:

Ultra-Low Memory Footprint: Idle Go containers hover around 15–30 MB of RAM, compared to Spring Boot's typical 500+ MB requirement.

Instantaneous Boot Times: Go binaries boot in milliseconds, allowing Kubernetes HPA (Horizontal Pod Autoscaler) to respond to sudden traffic spikes instantly.

Consistent Latency: Go’s concurrent garbage collector operates with sub-millisecond pauses, ensuring a flat, predictable latency curve for users hitting short link redirects.

Cons & Mitigations:

Manual Security / Auth Implementation: Go has no direct equivalent to a massive framework like Spring Security.

Mitigation: Because our API Gateway (Kong) handles JWT verification at the edge, the inner Go URL Service only needs to read a plain-text header injected by the gateway (X-User-Id), bypassing the need for a complex inner authentication framework. For token generation in the Auth service, standard libraries like golang-jwt/jwt and crypto/bcrypt can be easily implemented with minimal middleware.

Strict Ecosystem Shift: Developers transitioning from object-oriented languages must learn Go’s structural typing and explicit error handling models.

Mitigation: Establish strict coding standards and utilize Gin’s robust middleware community to standardize logging, recovery, and request validation.


## Cache

current choice: Redis

## Database:

current choice: Mysql with replication

