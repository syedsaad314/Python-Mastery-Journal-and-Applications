# Logic Breakdown: Follower Log Consistency Verification
**Engineer:** Syed Saad Bin Irfan

## The Problem
When network partitions clear or leaders change, followers can end up with uncommitted log entries from older terms that conflict with the new leader's log history.

## My Approach
I built a **Log Consistency Verification Engine** that implements Raft's log matching rules.

When a follower receives an `AppendEntries` request, it checks its log at `prev_log_index`. If it finds a term mismatch or a gap, it rejects the request. If it finds a conflict with the new entries at a later index, it deletes the mismatched entry and everything that follows it, overwriting its history with the leader's data to keep logs uniform across the cluster.

## Complexity Profile
* **Runtime Bounds:** Truncating and copying entries scales linearly at $O(C)$ relative to the number of conflicting or appended entries $C$.
* **Space Constraints:** Memory management shifts to $O(L)$ to hold the updated local log array.