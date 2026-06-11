# Logic Breakdown: Synchronous Read Repair Mechanism
**Engineer:** Syed Saad Bin Irfan

## The Problem
When network drops or partial failures occur, some replicas miss data updates. If left unmanaged, these nodes remain out of sync indefinitely, increasing the risk of data drift if background workers fail.

## My Approach
I implemented a **Synchronous Read Repair Engine**.

When a client requests a key, the coordinator reads the data from all available replicas. It inspects the version numbers attached to each response to find the newest value. Before returning that value to the client, the coordinator fires synchronous write operations to update any replicas that returned stale versions, bringing them up to speed.

## Complexity Profile
* **Runtime Bounds:** Resolving the latest version runs in $O(N)$ linear time relative to the number of replicas sampled.
* **Space Constraints:** Memory scales at $O(N)$ to hold the responses collected from the cluster.