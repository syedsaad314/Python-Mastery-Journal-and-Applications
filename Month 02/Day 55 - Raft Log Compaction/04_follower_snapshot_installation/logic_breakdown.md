# Logic Breakdown: Follower Snapshot Installation Handling
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When a follower receives a snapshot from the leader, it needs to safely overwrite its local history. It must clear out any old logs covered by the snapshot and update its tracking pointers without creating state conflicts.

## My Approach
I implemented a snapshot application sequence. The follower flushes its local log array, sets its local `commit_index` directly to the snapshot's `last_included_index`, and replaces its local data store with the leader's state snapshot.

## Complexity Profile
* Runtime Bounds: Clearing the log list and copying the snapshot runs in $O(S)$ time relative to state size.
* Space Constraints: Overwriting variables consumes $O(S)$ space for the new state data.