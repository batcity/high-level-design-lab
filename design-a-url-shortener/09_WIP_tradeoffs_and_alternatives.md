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


## Cache

current choice: Redis

## Database:

current choice: Mysql with replication

