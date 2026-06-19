# Logic Breakdown: Fencing Tokens Pattern
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Even with time-bound leases, an application could pause (e.g., during a long garbage collection cycle) causing its lease to expire. If the node wakes up later thinking it still holds the lock and attempts to write to storage, it will overwrite newer data written by a different node.

## My Approach
I engineered a **Monotonically Increasing Fencing Token System**.

Every time a lock is granted, the generator issues an increasing numerical token (e.g., 1, 2, 3). The storage engine records this token with every write. If a delayed write arrives with an older token than the last one processed, the storage engine rejects it immediately, protecting data integrity from late network packets.

## Complexity Profile
* **Runtime Bounds:** Token generation and storage verification run in $O(1)$ constant time.
* **Space Constraints:** Requires $O(1)$ constant space to track the boundary integer indices.