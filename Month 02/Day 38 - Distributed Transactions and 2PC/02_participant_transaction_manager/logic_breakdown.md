# Logic Breakdown: Participant Transaction State Guard rails
**Engineer:** Syed Saad Bin Irfan

## The Problem
A database shard cannot execute an update immediately when a transaction begins. It must first verify it has the necessary resources and lock them to prevent concurrent operations from changing the data before the transaction completes.

## My Approach
I designed a **Resource-Locking Participant Manager**.

When a prepare request arrives, the manager verifies data conditions (e.g., checking if a balance is sufficient). If the check passes, it acquires an exclusive resource lock and moves to the `PREPARED` state, promising to commit or abort the transaction based on the coordinator's final decision.

## Complexity Profile
* **Runtime Bounds:** Resource validation and lock assignments run in $O(1)$ constant time.
* **Space Constraints:** Memory footprint stays at $O(1)$ constant tracking space.