# Logic Breakdown: Replicated State Machine (RSM) Processing
**Engineer:** Syed Saad Bin Irfan

## The Problem
A distributed log is only useful if it can consistently update actual application state across different machines. The engine needs a reliable way to apply log entries to the local database safely, ensuring all nodes reach an identical internal state.

## My Approach
I built an isolated **Replicated State Machine (RSM)** engine driven by deterministic log processing loops.

The engine maintains a `last_applied_index` tracking pointer. When the cluster safely commits a log entry, the state machine reads the mutation string sequentially, parses the command parameters, and applies the changes directly to the underlying key-value dictionary. Because every node processes the exact same sequence of committed logs starting from the same initial state, they are guaranteed to remain perfectly uniform.

## Complexity Profile
* **Runtime Bounds:** Applying logs scales linearly ($O(C)$) based on the number of unapplied entries processed.
* **Space Constraints:** Memory usage scales with the total number of unique keys stored in the database.