# Engineering Log Overview: Distributed Consistent Hash Subsystem
**Lead Engineer:** Syed Saad Bin Irfan

## 1. The Core Problem
Traditional hashing techniques ($hash(key) \pmod N$) break down when scaling out distributed systems. Adding or removing a database node shifts almost all key positions across the cluster, causing massive, expensive data migrations that degrade network performance.

## 2. Architectural Brainstorming & Trade-offs
To build a scalable routing engine, we mapped both data keys and server nodes into a shared 32-bit integer token space ($0 \text{ to } 2^{32}-1$), visually forming a continuous logical ring.

### The Hotspot & Virtualization Dilemma
* **The Vulnerability:** Random physical node placement can leave large gaps on the ring, causing uneven data distribution.
* **The Fix:** We integrated Virtual Nodes (VNodes). Each physical machine maps to multiple points on the ring, creating uniform coverage and evenly balancing data distribution across all physical nodes.
* **Bounded Load Optimization:** To handle viral keys, we added strict capacity ceilings. If a primary node hits its limit, requests automatically cascade to the next available node down the ring.

## 3. Engineering Implementation Details
* **Fast Lookups via Binary Search:** We used Python's `bisect` library to look up key positions on the ring in $O(\log V)$ time.
* **Distinct Physical Replication:** Replicas are placed by moving clockwise along the ring, filtering out duplicate VNodes to ensure data is duplicated across distinct physical servers for high availability.