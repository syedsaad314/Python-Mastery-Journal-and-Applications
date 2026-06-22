# Logic Breakdown: Two-Phase Commit (2PC) Execution Engine
**Engineer:** Syed Saad Bin Irfan

## The Problem
If a network failure or node error interrupts a multi-node transaction mid-way, the system risks updating one partition while leaving another unchanged, violating data isolation and consistency rules.

## My Approach
I built a complete **Two-Phase Commit Protocol Engine**.

The engine forces atomic execution across independent storage nodes using a two-step boundary:
1. **Prepare Stage:** Nodes dry-run the operation and hold data changes in a temporary staging buffer.
2. **Commit Stage:** If all nodes report a successful dry-run, the coordinator sends a final commit instruction to finalize the changes. If any node fails the dry-run, the coordinator sends an abort instruction, clearing out the staged changes across all nodes.

## Complexity Profile
* **Runtime Bounds:** Executing the transaction requires two communication round-trips to all nodes, taking $O(N)$ time for $N$ shards.
* **Space Constraints:** Memory usage scales linearly at $O(M)$ to hold the $M$ mutations inside the staged data dictionaries.