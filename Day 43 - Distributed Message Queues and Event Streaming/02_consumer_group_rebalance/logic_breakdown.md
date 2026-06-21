# Logic Breakdown: Consumer Group Partition Rebalancing
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When application consumer instances spin up or crash unexpectedly, partition assignments must adjust dynamically to keep processing data without causing duplicate reads or letting partitions go unserved.

## My Approach
I built a **Consumer Group Partition Rebalance Coordinator**.

The design uses a round-robin assignment mapping strategy. When a consumer node joins or leaves the group, the coordinator recalculates partition distribution across the remaining active nodes. This guarantees that each partition is processed by exactly one consumer in the group at any given time, preventing message processing collisions.

## Complexity Profile
* **Runtime Bounds:** Partition rebalancing scales linearly at $O(P)$ relative to total partition count $P$.
* **Space Constraints:** Assignment allocations require linear $O(C + P)$ tracking space.