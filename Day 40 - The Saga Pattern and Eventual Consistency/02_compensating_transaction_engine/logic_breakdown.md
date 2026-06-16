# Logic Breakdown: Asynchronous Backward Compensation Loops
**Engineer:** Syed Saad Bin Irfan

## The Problem
Since the Saga pattern commits local transactions immediately to keep resources free, standard database rollbacks won't work if a downstream step fails. We need a way to explicitly undo changes that were already committed.

## My Approach
I engineered a **LIFO (Last-In-First-Out) Reversal Compensation Engine**.

The engine tracks successful forward actions in an execution log. If a failure occurs, it reads this log backward, mapping each completed action to its matching compensating routine (e.g., matching a charge action to a refund routine). Processing the rollback in reverse order ensures dependencies are unrolled safely without breaking data consistency.

## Complexity Profile
* **Runtime Bounds:** Reversing history scales linearly at $O(K)$ time, where $K$ is the number of steps completed before the failure.
* **Space Constraints:** Tracks completed operations inside an $O(K)$ storage history log.