# Logic Breakdown: Log Matching Property Verification
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Raft relies on an inductive safety rule: if two separate node logs share an entry with the identical index and term, those logs are guaranteed to be identical from index 1 up to that point. We need a way to enforce this rule whenever a message arrives.

## My Approach
I built an entry validation gate. It inspects the record at the index just before the incoming updates (`prev_log_index`). If that local entry doesn't match the leader's term, the update is rejected, signaling that the follower needs to align its log history.

## Complexity Profile
* Runtime Bounds: Structural index checking evaluates in $O(1)$ time.
* Space Constraints: Runs inline without additional heap allocations, using $O(1)$ space.