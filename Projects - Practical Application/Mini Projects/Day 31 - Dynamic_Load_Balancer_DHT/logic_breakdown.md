# Portfolio Code Review: Layer-7 Consistent Hashing Load Balancer
**Author:** Syed Saad Bin Irfan

## Practical Context
This load balancer uses consistent hashing to implement sticky sessions (like those in NGINX or HAProxy), ensuring that requests from the same client IP consistently land on the same backend server without needing a stateful session database.

## Engineering Standards Applied
* **Stateless Sticky Sessions:** Routes clients based purely on their IP address hash. This ensures a client keeps hitting the same backend server, maintaining session affinity without the memory overhead of a shared tracking store.
* **Deterministic Failover Handling:** When a backend server crashes, only the clients mapped to that specific node are rebalanced. Traffic for all other servers remains undisturbed, preventing global session dropouts.
* **Scalable Ring Traversal:** Uses the standard `bisect` library to run lookups in $O(\log N)$ time, allowing the load balancer to route packets quickly even with hundreds of backend nodes.