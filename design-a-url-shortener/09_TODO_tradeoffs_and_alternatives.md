# Tradeoffs and alternatives:

Think in terms of system pressures

A useful way to discover trade-offs is to repeatedly ask:

1. What problem does this choice solve?
2. What new problem does this choice create?
3. What simpler alternative exists?
4. Why wasn’t the simpler option enough?
5. What does this system optimize for?
6. When would this design stop working?

## API Gateway

**Current choice:** kong

**What problem does this choice solve:** The Idea is to distribute traffic across different servers in order to handle a large number of users, the additional benefit here is reliability since having a single web server would introduce a single point of failure

So it addresses two major system pressures

- Reliability
- Throughput / Traffic

Also think about why you chose a gateway instead of a load balancer

**What new problem does this choice create:** I've substituted one single point of failure for another here, if the API gateway is down then the entire service would be down

I've also introduced additional complexity since devs would need to maintain the API gateway

**What simpler alternative exists?** 





## URL shortener service, User Authenticaton Service

current choice: Java + Spring boot


## Cache

current choice: Redis

## Database:

current choice: Mysql with replication

