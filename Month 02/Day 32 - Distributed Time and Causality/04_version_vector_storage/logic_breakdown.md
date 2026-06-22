# Logic Breakdown: Version Vector Database Partition Partitioning
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a database allows updates on multiple master nodes simultaneously, network partitions can cause nodes to accept different values for the same key. The storage layer must be able to detect these overlapping updates rather than blindly overwriting data.

## My Approach
I built a **Conflict-Aware Versioned Storage Cell** inspired by DynamoDB's sibling collection model.

Instead of keeping only a single raw string, the storage cell tracks a map of historical versions keyed by their specific version vectors. When a new write arrives, it is evaluated against all active versions. If the write is an ancestor, it is ignored; if it is a clear successor, it replaces the old version. If the write occurred concurrently, the system retains both values as **siblings**, allowing the client application to safely resolve the conflict later.

## Complexity Profile
* **Runtime Bounds:** Write evaluations run in $O(S \cdot N)$ time, where $S$ is the number of active sibling variants and $N$ is the number of unique tracking nodes in the vector.
* **Space Constraints:** Scales at $O(S \cdot N)$ to store sibling values alongside their version vector metadata.