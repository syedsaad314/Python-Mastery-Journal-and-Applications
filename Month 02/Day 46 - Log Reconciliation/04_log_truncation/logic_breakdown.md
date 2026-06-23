# Logic Breakdown: Log Truncation Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Uncommitted log entries that conflict with the leader's validated log history must be permanently deleted from follower storage to prevent data corruption.

## My Approach
I implemented a safe slice truncation mechanism. It safely trims off uncommitted or conflicting log slices from the first point of divergence onward, preparing the node's local storage array to receive the correct log history from the leader.

## Complexity Profile
* Runtime Bounds: Truncating arrays via slicing scales at linear $O(K)$ time relative to pruned slice size $K$.
* Space Constraints: Slicing creates an updated array map bounding space utilization to $O(L)$ log length.