# Logic Breakdown: Time-Bound Lease Management
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a distributed node acquires a permanent lock on a database row and suddenly crashes or loses its network connection, that lock remains active forever, creating a permanent deadlock across the entire cluster.

## My Approach
I implemented a **Time-Bound Ephemeral Lease Mechanism**.

Instead of granting indefinite locks, the system assigns locks with an explicit time-to-live (TTL) timestamp. If a node fails to release the lock within the specified lease window, the lease expires naturally. This allows healthy nodes to claim the resource and ensures the system remains available.

## Complexity Profile
* **Runtime Bounds:** Lease validation and acquisition checks execute in $O(1)$ constant time.
* **Space Constraints:** Operates under a strict $O(1)$ constant memory overhead footprint.