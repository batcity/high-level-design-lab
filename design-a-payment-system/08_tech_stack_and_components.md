# Tech Stack and Components:

## Load Balancer:

The load balancer choice isn't hugely important here, any popular one would do; examples: HAProxy, Envoy, Cloudflare load balancer etc

TODO: AI says a good load balancer for this scenario requires the following -> understand why?

Ideally the load balancer should explicitly support the following features:

- TLS termination (Transport layer security) -> here's a good writeup on TLS termination and its benefits -> https://www.haproxy.com/glossary/what-is-ssl-tls-termination

- Request timeouts

    This video is a good resource on Request timeouts within the context of load balancers -> https://www.youtube.com/watch?v=uNjACLXoH5A

    This is also a good resouce: https://my.f5.com/manage/s/article/K000146636

    Here's the different types of Timeouts:

    - Client/load balancer timeout

      Each connection with the client takes up some resources, the load balancer should be able to close out unused connections so that these resources are reclaimed

    - load balancer/Server timeout

      Each connection with the server also takes up some resources, if the backend server takes too long to respond then the load balancer can enforce timeouts to prevent resource wastage

-  Circuit breaking

- Connection limits (protect downstream during provider slowness)
- Health checks with fast failover

## Payment Service:

- The payment service would be built with Java and Spring boot since this combination is used widely in enterprise and is known to be secure and stable which is highly important for financial services

## Database:

- The payment data needs to be highly consistent, so MySQL is a good choice here since the total storage requirement would only be 91 GB for the next 5 years based on estimates from the back of the envelope calculations