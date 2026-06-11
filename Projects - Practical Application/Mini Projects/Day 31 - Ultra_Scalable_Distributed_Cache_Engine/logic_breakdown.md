# Portfolio Code Review: Ultra-Scalable Distributed Cache Engine with Hotspot Mitigation
**Author:** Syed Saad Bin Irfan

## Practical Context
This engine simulates a distributed caching layer (similar to the internal mechanics of Redis Cluster or Memcached) designed to partition large datasets horizontally across multiple servers while protecting individual nodes from traffic spikes.

## Engineering Standards Applied
* **Dynamic Load Shedding:** Tracks per-node request rates to detect hotspots. When a server becomes overloaded, the engine automatically routes traffic to a fallback node, preventing cascading failures.
* **Granular Ring Balancing:** Uses 120 virtual nodes per physical machine to ensure keys are evenly distributed across the entire cluster, maximizing cache efficiency and memory utilization.
* **Graceful Failover Handling:** Isolates node management logic from data operations, allowing you to add or remove servers on the fly without causing cluster downtime or breaking cache lookups.