## Back-of-the-Envelope Calculations

Here's the **storage and traffic requirements** for a URL shortener:

- **Worst-case total URLs:** 10M users × 100 URLs = 1B URLs  
- **Storage per URL:** ~120 bytes (original URL + short URL + metadata)  
- **Total storage:** 1B × 120 bytes ≈ ~120 GB  
- **Peak QPS estimate:**  
  - URL creations: 2M/day → ~23 QPS average  
  - Redirects: 20M/day → ~230 QPS average, higher at peak concurrent usage  

> These numbers provide order-of-magnitude guidance for database sizing, caching, and load balancing.