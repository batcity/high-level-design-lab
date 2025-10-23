## Assumptions & Scale

The following assumptions provide baseline inputs for sizing and architecture decisions. They describe expected usage patterns and system inputs.

- **Users:** 10M MAU, 2M DAU, peak 200k concurrent  
- **URLs per user:** Up to 100 URLs per user; average user ~5–10 URLs  
- **URL length:** Average original URL ~100 bytes; short URL ~8–10 characters (~10 bytes)  
- **Read/write ratio:** ~10:1 (redirects:creations)  
- **Traffic:** ~2M URL creations/day; redirects ~20M/day  
- **Caching:** Hot cache for popular URLs to reduce database load  
- **Retention / TTL:** Optional expiration after 1 year to limit dataset growth 