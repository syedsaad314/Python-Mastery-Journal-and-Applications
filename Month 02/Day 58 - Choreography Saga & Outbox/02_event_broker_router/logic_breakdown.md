# Logic Breakdown: Event Broker Router Simulation
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Choreographed architectures require a central, non-blocking delivery loop. If a publisher blocks its execution frame while waiting for a consumer to ingest a message, the system loses the core scaling benefit of asynchronous microservices.

## My Approach
I engineered an asynchronous event channel registry using `asyncio.gather`. Services can dynamically hook into specific topics, and when an event lands, the router fans it out to all subscribers in parallel without blocking the sender.

## Complexity Profile
* Runtime Bounds: Routing triggers in O(S) time, where S represents the count of active topic subscribers.
* Space Constraints: Internal map pointers grow linearly at O(T * S) for total topics and registrations.