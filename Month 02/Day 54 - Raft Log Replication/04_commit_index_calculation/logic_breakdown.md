# Logic Breakdown: Commit Index Consensus Calculus
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
A leader cannot simply mark an entry as committed as soon as it is appended locally. It must wait until a majority of cluster nodes have securely written that entry to their logs before considering it finalized.

## My Approach
I utilized a median-sorting algorithm across the cluster's replication pointers (`match_indices`). Sorting the progress pointers ensures that any index landing at or below the median position has been successfully written to a majority of nodes.

## Complexity Profile
* Runtime Bounds: Sorting the cluster pointers scales at $O(N \log N)$ based on the cluster node count $N$.
* Space Constraints: Copying the map values into a list uses $O(N)$ memory space.