# Logic Breakdown: Quorum Commit Index Computation
**Engineer:** Syed Saad Bin Irfan

## The Problem
A leader cannot mark a log entry as committed based on its local state alone. It must trace exactly how far its followers have replicated the log to avoid losing data if a failure occurs before a majority secures the entry.

## My Approach
I engineered a **Quorum Commit Tracker Engine** based on sorting match indices.

The leader tracks each peer's progress using a `match_index` map. To find the highest safe commit point, the engine collects these indices and sorts them. The median value represents the highest log index that has been successfully replicated to a strict majority of nodes, providing a safe line for transaction execution.

## Complexity Profile
* **Runtime Bounds:** Sorting the node index array takes $O(N \log N)$ time for a cluster of size $N$.
* **Space Constraints:** Tracks allocations in $O(N)$ space to maintain state maps for all nodes.