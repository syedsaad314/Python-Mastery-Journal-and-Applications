# Logic Breakdown: Peer-to-Peer Cooperative Recovery Protocol
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a coordinator crashes mid-transaction, standard protocols freeze to prevent data conflicts. To remain non-blocking, surviving nodes need a safe way to determine the correct outcome by communicating directly with each other.

## My Approach
I built a **Peer-to-Peer Cooperative Recovery Coordinator**.

When surviving nodes detect a coordinator failure, they pick a temporary leader and pool their states. The engine evaluates the cluster state using 3PC consensus rules: if even one node reached the `PRE_COMMIT` phase, it proves every node voted yes, making it safe to commit. If no node reached pre-commit, the cluster defaults to an abort, safely releasing locks without blocking.

## Complexity Profile
* **Runtime Bounds:** Analyzing peer states scales linearly at $O(P)$ for $P$ surviving nodes.
* **Space Constraints:** State tracking structures require $O(P)$ memory footprint.