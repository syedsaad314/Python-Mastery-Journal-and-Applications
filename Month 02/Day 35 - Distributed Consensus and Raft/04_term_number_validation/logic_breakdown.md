# Logic Breakdown: Monotonic Term Number Validation
**Engineer:** Syed Saad Bin Irfan

## The Problem
In distributed networks, network partitions can isolate nodes, creating "split-brain" scenarios. An old leader might get cut off from the network and continue trying to process updates while the rest of the cluster elects a new leader with a higher term counter.

## My Approach
I implemented a **Monotonic Term Number Validator Engine**.

Terms act as a logical clock in Raft. Every message carries the sender's current term number. If a node detects an incoming message with a term greater than its own, it updates its local term to match. If an old leader discovers a higher term counter, it immediately steps down and reverts to a follower, safely resolving split-brain conflicts.

## Complexity Profile
* **Runtime Bounds:** Term validation checks complete in $O(1)$ execution time.
* **Space Constraints:** Requires $O(1)$ constant tracking memory.