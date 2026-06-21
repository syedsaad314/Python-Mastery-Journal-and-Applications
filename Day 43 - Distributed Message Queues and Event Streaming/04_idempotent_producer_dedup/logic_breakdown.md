# Logic Breakdown: Idempotent Producer Write Deduplication
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When network timeouts happen, a producer might retry sending a message that the broker actually already received and saved. Without proper safety guards, this causes duplicate events to flood downstream systems.

## My Approach
I developed an **Idempotent Producer Write Deduplication Interceptor**.

The interceptor requires each producer to attach a unique ID and an incremental sequence number to every message packet. The broker tracks the highest sequence number processed for each producer ID. If a retried message arrives with an old or duplicate sequence number, the broker drops it instantly, preventing duplicate records from corrupting the system.

## Complexity Profile
* **Runtime Bounds:** Sequence verification and tracking updates run in $O(1)$ constant time.
* **Space Constraints:** Memory scales at $O(M)$ where $M$ is the number of unique active producers.