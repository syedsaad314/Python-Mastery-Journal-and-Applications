# Logic Breakdown: Follower Log Conflict Truncation
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a leader crashes mid-broadcast, followers can be left with uncommitted, conflicting log entries. When a new leader takes over, it must clean up these stale paths and force all nodes into perfect alignment.

## My Approach
I designed a conflict-detection sweep. As incoming entries are processed, the follower compares terms at each index. If a term mismatch is found, the follower truncates its log at that point, discarding the stale history and appending the leader's authoritative updates.

## Complexity Profile
* Runtime Bounds: Slicing and updating the log array runs in $O(R)$ time relative to the number of overwritten records.
* Space Constraints: Allocates memory linearly at $O(R)$ during the slicing and truncation step.