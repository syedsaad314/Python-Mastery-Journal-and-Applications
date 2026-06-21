# Logic Breakdown: Message Delivery Guarantee Semantics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Designing distributed streams requires managing trade-offs between delivery guarantees. The system must decide how to handle failures without losing data or creating duplicate entries.

## My Approach
I engineered a **Delivery Guarantee Semantics Simulator**.

The simulator models two core patterns:
1. **At-Least-Once:** Data is processed first, and the offset is committed afterward. This guarantees no data loss, but can introduce duplicate records if the system crashes right before saving the offset.
2. **Exactly-Once:** Data mutations and offset saves are processed together atomically in a single transaction block. If a crash occurs midway, the entire transaction rolls back, preventing both data loss and duplicate processing.

## Complexity Profile
* **Runtime Bounds:** Condition checking and execution loops run in $O(1)$ constant time.
* **Space Constraints:** Operates cleanly within an $O(1)$ constant memory overhead footprint.