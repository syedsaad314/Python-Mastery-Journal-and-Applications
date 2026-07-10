# Logic Breakdown: Transaction Abort & Rollback Logic
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a transaction fails during the voting phase, participants that have already allocated locks or reserved resources for that transaction cannot leave them hanging indefinitely. The cluster must clean up these temporary workspaces to free up system resources.

## My Approach
I implemented a structural rollback engine. When an abort condition is triggered, it loops through the registered participants, clears out temporary transactional memory entries, and releases any pending locks to revert the cluster back to its pre-transaction state.

## Complexity Profile
* Runtime Bounds: Clears participant workspaces in linear time $O(P)$ relative to the participant count.
* Space Constraints: Tracks the cleanup operations using $O(P)$ log entries.