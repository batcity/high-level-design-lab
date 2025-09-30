# Non-functional Requirements

- P95 end-to-end message latency: <200 ms intra-region <500 ms cross-region  
- Availability: 99.99%  
- Durability: 11 nines for message storage until all recipients ack 
- Scale assumptions (for sizing, not limits):  
 **  2B MAU, 500M DAU, peak 50M concurrent  
 ** Peak ingress(user-to-server write traffic): 25M msgs/sec global; fanout average 1.8x (due to groups)  
 ** Media: 70 PB stored, 20 Tbps egress peak 

 ## Constraints:

- E2EE (end to end encryption): servers are blind to content; only metadata can be inspected  
- Mobile-first networks: high packet loss, intermittent connectivity  
- Cost: optimize cross-region traffic and storage hot/cold tiers