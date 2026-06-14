# Logic Breakdown: Log Compaction Checkpoint Baseline
**Engineer:** Syed Saad Bin Irfan

## The Problem
In long-running production systems, append-only logs grow indefinitely. Over time, they consume all available disk space and make node restarts incredibly slow, as replaying millions of entries takes too long.

## My Approach
I modeled a **Log Compaction and Truncation Engine Framework**.

Instead of keeping every historic entry, the engine takes a snapshot of the current state and discards obsolete intermediate log entries (e.g., dropping `x=1` because a later entry set `x=2`). The system truncates the log up to the checkpoint index while preserving the latest metadata boundary markers (`last_included_index` and `last_included_term`) to give lagging nodes the context they need to sync up.

## Complexity Profile
* **Runtime Bounds:** Truncating arrays scales linearly at $O(R)$ relative to the number of remaining entries $R$ kept in the active log window.
* **Space Constraints:** Optimizes memory space, dropping storage usage from $O(E)$ historical logs to a compact $O(S)$ state size representation.