# Logic Breakdown: Partitioned Cluster Recovery Loops
**Engineer:** Syed Saad Bin Irfan

## The Problem
Once a network partition clears, isolated nodes will reappear with outdated or conflicting logs. The cluster must automatically detect these discrepancies, resolve the conflicts, and bring all nodes back into perfect alignment.

## My Approach
I modeled a **Partitioned Cluster Recovery Coordinator**.

When the network partition heals, the recovered nodes reconnect to the active leader. By comparing log positions and terms, the leader detects gaps and streams the missing updates to the out-of-sync followers. This alignment process updates the stale nodes smoothly, ensuring data consistency across the entire cluster.

## Complexity Profile
* **Runtime Bounds:** Reconciling logs scales linearly at $O(M)$ relative to the number of missing entries $M$.
* **Space Constraints:** Allocations scale at $O(L)$ to store the updated log array elements.