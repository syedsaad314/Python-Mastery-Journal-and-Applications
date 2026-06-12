# Logic Breakdown: Distributed Lock Manager (DLM) Basics
**Engineer:** Syed Saad Bin Irfan

## The Problem
When multiple transactions try to update overlapping data keys across a sharded cluster simultaneously, they can cause race conditions, split-brain states, or dirty read errors.

## My Approach
I designed a **Mutual Exclusion Lock Registry Framework**.

The manager tracks resource ownership across the cluster using an assignment map. Workers must explicitly request and acquire an exclusive token for a data key before changing it. This structure isolates concurrent transactions and prevents conflicting updates from executing simultaneously on the underlying storage nodes.

## Complexity Profile
* **Runtime Bounds:** Claiming or releasing a resource token runs in $O(1)$ constant time via dictionary lookups.
* **Space Constraints:** Memory scales at $O(L)$ linear space relative to the total number of active locks $L$ currently held by the cluster.