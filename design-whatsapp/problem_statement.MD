# Problem framing:

Design WhatsApp (core messaging). Scope only what’s needed for a v1 that still feels “WhatsApp-y”.

## In-scope features / Functional Requirements

- 1:1 chats, group chats (up to 1,024 members)  
- Text, images, videos, voice notes (media up to 100 MB)
- Delivery receipts (✓ sent, ✓✓ delivered, ✓✓ blue read)  
- Presence (online/last seen/typing), push notifications  
- End-to-end encryption (Signal protocol family)  
- Multi-device (phone + up to 3 companion devices)  
- Offline support and message ordering  

## Non-functional Requirements

- P95 end-to-end message latency: <200 ms intra-region <500 ms cross-region  
- Availability: 99.99%  
- Durability: 11 nines for message storage until all recipients ack 
- Scale assumptions (for sizing, not limits):  
 **  2B MAU, 500M DAU, peak 50M concurrent  
 ** Peak ingress: 25M msgs/sec global; fanout average 1.8x (due to groups)  
 ** Media: 70 PB stored, 20 Tbps egress peak  

## Constraints:

- E2EE (end to end encryption): servers are blind to content; only metadata can be inspected  
- Mobile-first networks: high packet loss, intermittent connectivity  
- Cost: optimize cross-region traffic and storage hot/cold tiers