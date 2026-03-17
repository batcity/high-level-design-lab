# Tech Stack and Components:

## Load Balancer:

The load balancer choice isn't hugely important here, any popular one would do; examples: HAProxy, Envoy, Cloudflare load balancer etc

Ideally the load balancer should explicitly support the following features:

- TLS termination (Transport layer security) -> here's a good writeup on TLS termination and its benefits -> https://www.haproxy.com/glossary/what-is-ssl-tls-termination

- Request timeouts:

    This video is a good resource on Request timeouts within the context of load balancers -> https://www.youtube.com/watch?v=uNjACLXoH5A

    This is also a good resouce: https://my.f5.com/manage/s/article/K000146636

    Here's the different types of Timeouts:

    - Client/load balancer timeout

      Each connection with the client takes up some resources, the load balancer should be able to close out unused connections so that these resources are reclaimed

    - load balancer/Server timeout

      Each connection with the server also takes up some resources, if the backend server takes too long to respond then the load balancer can enforce timeouts to prevent resource wastage

-  Circuit breaking:

    The idea with circuit breaking is that if a backend service hits a certain number of failures then the load balancer would stop sending requests to that service, this is useful in a couple of ways

      - latency reduction - The backend service might take a while to fail, this time can be saved by immediately returning a failure from the load balancer, this has the additional benefit of freeing up load balancer resources

      - cascading failures - sending more requests to a very slow backend service could cause a negative spiral on the backend service where requests start piling up and resources dry up; this might trigger a worse crash that might otherwise be temporary, the circuit breaker would provide breathing room to the backend service in order to clear up existing requests

    Here's some documentation on circuit breakers: https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/circuit-breakers/

- Connection limits:

  Some Load balancers let you set the maximum number of concurrent connections that the load balancer or the backend server can have at a single point of time, this helps avoid scenarios where too many connections cause increased CPU or memory pressure on the server

  For example: Imagine a scenario where the provider that actually completes the payments is slow, in this case several connections can pile up causing the backend server to go down due to high resource usage 

  Here's some documentation on connection limits: https://www.haproxy.com/documentation/haproxy-configuration-tutorials/performance/overload-protection/

- Health checks with fast failover:

  Health checks are standard checks which help ensure that the backend service the load balancer is serving requests to is still healthy, failover lets developers reroute the requests to a backup server in-case one of the backend servers isn't healthy

  Here's documentation on health checks: https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/


  and failovers: https://www.haproxy.com/blog/failover-and-worst-case-management-with-haproxy

## Payment Service:

- The payment service would be built with Java and Spring boot since this combination is used widely in enterprise and is known to be secure and stable which is highly important for financial services

## Database:

- The payment data needs to be highly consistent, so MySQL is a good choice here since the total storage requirement would only be 91 GB for the next 5 years based on estimates from the back of the envelope calculations