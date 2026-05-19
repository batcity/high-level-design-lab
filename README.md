# high-level-design-lab  

A personal collection of **system design explorations, diagrams, and notes** as I learn how to design scalable, reliable, and secure systems.  

Each folder covers a different system (e.g., WhatsApp, YouTube, Twitter), documenting the **problem framing, assumptions, architecture, trade-offs, and key learnings**.  

📌 **Goal:** Build a structured knowledge base of system design **patterns, practices, and back-of-the-envelope reasoning** that I can reuse for interviews and real-world design work.  

⚡ **Note:** These designs are for **learning and discussion** purposes. I’ve used a mix of research, reading, and AI-assisted reasoning to refine them.  


## Repository Structure

The repo is split into a few major sections:

```txt
design-*/                     -> Complete system design case studies
architectural-primitives/     -> Reusable distributed systems patterns
implementations/              -> Small implementation examples / experiments
cheat-sheets/                 -> Quick reference notes
```



## System Design Case Studies


Each system write-up follows the same template for consistency:  

1. **Problem statement** – What we’re building and the scope.  
2. **Assumptions & scale** – Traffic, users, constraints.  
3. **Back-of-the-envelope calculations** – Storage, throughput, latency.  
4. **Non-functional requirements** – Latency, availability, durability, cost.  
5. **Data model / DB schema sketch** – Core entities and relationships.  
6. **System architecture diagram** – High-level components and interactions.  
7. **Critical flows** – E.g., message send, media upload, feed generation.  
8. **Tech stack and components** - Key technologies and frameworks for each layer.
9. **Trade-offs & alternatives** – Different approaches and design choices.  
10. **Extensions / next steps** – Features or improvements not in v1.  

## Architectural Primitives

The `architectural-primitives/` folder contains reusable concepts and patterns that appear across many distributed systems.

These are the **building blocks** used repeatedly in larger architectures.

## Why this repo?  

- Build intuition for **scalability and reliability**.  
- Practice **structured thinking** under interview-style time limits.  
- Create a **reusable library** of design blueprints and patterns.  
