# Distributed Consistent Hash Engine

## Operational Architecture & Topology Invariants
* **Consistent Ring Topology**: Maps keys and nodes into a 32-bit integer space to minimize data migration during cluster resizing.
* **Hotspot Mitigation via VNodes**: Uses multiple virtual positions per physical server to ensure balanced, uniform data distribution.
* **Bounded Load Guarantees**: Enforces strict capacity limits per node, automatically cascading excess traffic to adjacent nodes along the ring to handle popular keys safely.

## Component Overview
* `models.py`: Declares structures for host configs and routing results.
* `hash_ring.py`: Implements token distribution, binary search routing, and load tracking.
* `node_manager.py`: Mocks storage backends for virtual hosts.