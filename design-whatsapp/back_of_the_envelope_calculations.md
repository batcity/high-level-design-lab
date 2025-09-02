# Back of the Envelope estimates:

This document provides a rough storage model for a messaging platform like whatsapp with **2 billion monthly active users (MAUs)**.  

Two main categories of content need to be stored:

1. **Messages** – plain text.  
2. **Media** – photos, images, GIFs, documents, etc. (not covered in detail here).  

---

## Message Storage Assumptions

- **Users:** 2 billion daily active users (DAUs).  
- **Messages per User:** 10 messages/day → ~300 messages/month.  
- **Message Size:** 300 characters (≈300 bytes, assuming ASCII).  
  - Note: UTF-8 or other encodings may increase the footprint depending on character set.  
- **Metadata Overhead:** ~50% of message size (sender/receiver IDs, timestamps, delivery/read receipts, encryption headers, etc.).  
- **Durability:** Replication factor of 3 (standard practice for fault tolerance and high availability).  

> **Disclaimer:** These assumptions are for *order-of-magnitude estimation only*. They are not based on real-world WhatsApp statistics.  

---

## Storage Calculation

1. **Per Message:**  
   - 300 bytes (text) + 150 bytes (metadata) = **450 bytes**.  

2. **Per User (monthly):**  
   - 300 messages × 450 bytes = **0.135 MB**.  

3. **All Users (monthly, raw):**  
   - 0.135 MB × 2B users = **270 TB**.  

4. **All Users (monthly, with replication):**  
   - 270 TB × 3 = **810 TB**.  

---

## Conclusion

A messaging system with 2B DAUs would need to provision **~810 TB of storage per month** for text messages alone, not including media.  
