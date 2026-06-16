# Logic Breakdown: Choreographed Saga Event Bus Architecture
**Engineer:** Syed Saad Bin Irfan

## The Problem
A central orchestrator can become a single point of failure or a performance bottleneck in high-throughput systems. Choreographed sagas eliminate this by letting microservices coordinate transactions independently using events.

## My Approach
I engineered an **Asynchronous Choreography Event Bus Structure**.

In this design, services don't wait for explicit orders from a central manager. Instead, they subscribe to an event bus and react independently when an update occurs (e.g., the inventory service listens for an `ORDER_CREATED` event to adjust stock automatically). This approach keeps services decoupled and highly responsive.

## Complexity Profile
* **Runtime Bounds:** Publishing an event takes $O(S)$ time, where $S$ is the number of active subscribers listening to that event category.
* **Space Constraints:** Subscriber routing registries consume $O(E \times S)$ tracking space across events $E$.