# Tech Stack and Components:

## Load Balancer:

The load balancer choice isn't hugely important here, any popular one would do; examples: HAProxy, Envoy etc

TODO: AI says a good load balancer for this scenario requires the following -> understand why?

You want the load balancer to explicitly support:
TLS termination -> here's a good writeup on TLS termination -> https://www.haproxy.com/glossary/what-is-ssl-tls-termination
Request timeouts & circuit breaking
Connection limits (protect downstream during provider slowness)
Health checks with fast failover

## Payment Service:

- The payment service would be built with Java and Spring boot since this combination is used widely in enterprise and is known to be secure and stable which is highly important for financial services

## Database:

- The payment data needs to be highly consistent, so MySQL is a good choice here since the total storage requirement would only be 91 GB for the next 5 years based on estimates from the back of the envelope calculations