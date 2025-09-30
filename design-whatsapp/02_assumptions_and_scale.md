# Assumptions & Scale

The following assumptions provide order-of-magnitude inputs for design choices. They serve as the baseline context for sizing and architecture choices.

- **Users:** 2B MAU, 500M DAU, peak 50M concurrent  
- **Message traffic:** Peak ingress 25M msgs/sec global; average fanout 1.8× (due to groups)  
- **Media storage:** 70 PB stored, peak 20 Tbps egress  
- **Network constraints:** Mobile-first, high packet loss, intermittent connectivity  
- **Security constraints:** End-to-end encryption (servers blind to content; only metadata visible)  
- **Cost considerations:** Minimize cross-region traffic, use hot/cold storage tiers  