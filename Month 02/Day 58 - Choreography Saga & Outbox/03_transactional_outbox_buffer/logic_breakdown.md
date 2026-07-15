# Logic Breakdown: Transactional Outbox Buffer
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
The "dual-write problem" occurs when a microservice writes to its database and then attempts to broadcast a network event. If the network drops or the broker crashes mid-flight, the database change sticks but the rest of the ecosystem never hears about it, leading to fractured systems.

## My Approach
I simulated the Transactional Outbox Pattern. Instead of sending network messages mid-flight, the application writes both the business entity updates and the outbound event message into the same database transaction. A separate process then sweeps this outbox table to guarantee reliable event delivery.

## Complexity Profile
* Runtime Bounds: Appends and sweeps execute within O(1) and O(P) respectively, where P tracks the size of pending logs.
* Space Constraints: Buffers expand at O(U) relative to the number of un-swept event messages.