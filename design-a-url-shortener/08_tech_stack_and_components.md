# Tech Stack and Components

This section outlines the recommended technologies for building a **URL shortener** that can scale to 10M MAU (Monthly active users).  


## API Gateway

The gateway should perform both redirects to the appropriate microservice and JWT authentication for protected endpoints, the API gateway also needs to handle a large amount of traffic

Given these requirements, Kong is a popular and highly compatible open-source option that fits the use case well. It offers the following features that make it an appropriate pick

- JWT authentication
- 50K+ transactions per second per node it's deployed in

## Services

All backend components are implemented as **stateless microservices**, deployed in containers and orchestrated via **Kubernetes**. Java / Spring Boot is a mature toolset for building these services

---

### Services Overview

| Service | Primary Language | Purpose |
|----------|------------------|----------|
| **User Authentication Service** | **Java (Spring Boot)** | Handles user authentication, JWT token issuance |
| **URL shortener Service** | **Java (Spring Boot)** | Manages user profiles, converting long URLs to short ones, managing stored URLs for registered users. |

## Cache

Both Memcached and Redis are valid options for the caching system. They offer extremely high performance for simple key-value lookups (required for redirection).

However, they are not identical. In the event that we need advanced capabilities like analytics or a counter to track the number of times each short code is accessed, Redis is the superior choice because it natively supports:

1. Atomic Operations (e.g., the INCR command), which guarantee accurate, concurrent click counting without database contention or race conditions.

2. Complex Data Structures (e.g., Sorted Sets), which allow for the efficient, real-time maintenance of leaderboards and advanced analytics directly within the cache layer.

## Database (MySQL with Replication):

The database permanently stores all user information and the link mapping data. MySQL is a solid, industry-standard choice.

### Required Data: 

User accounts, user-saved URLs, and the core short code → long URL mapping

### Scaling & High Availability

**QPS estimate:**

- **Traffic estimate:** ~2M URL creations/day; redirects ~20M/day
- **Write QPS**: 46 (Math: 2 million url creations/12 hours/60 mins/60 seconds)
- **Read QPS**: 462 (Math: 20 million url creations/12 hours/60 mins/60 seconds)
- **QPS**: Read + write QPS = ~500
- **Peek QPS** = 2 * QPS = ~1000

While the estimated traffic (around 1000 QPS hitting the database) is moderate, high availability (avoiding downtime) is essential.

> Note: The QPS estimate that the database would see is much higher than what it's actually going to be since there's a cache that sits above it but I've ignored that to make estimates a bit less complicated

**High Availability:**  
A Leader-Follower setup will be used. This avoids a Single Point of Failure by having a copy of the database ready to take over immediately if the primary server fails.

**Traffic Offloading:**  
The Leader server handles all Writes (new link creation), and the Follower server handles the small number of Read queries (cache misses). This distribution ensures high performance and readiness for future growth.
