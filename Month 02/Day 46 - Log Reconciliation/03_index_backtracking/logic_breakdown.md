# Logic Breakdown: Index Backtracking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
A leader must find out where a follower's log matches its own without dragging down the network by sending the entire historical log array at once.

## My Approach
I implemented a stateful backtracking pointer mechanism. The leader maintains a next_index variable for each peer. If a replication request fails due to an inconsistency, the pointer decrements systematically, narrowing down the search window until a common consensus point is found.

## Complexity Profile
* Runtime Bounds: Decrements complete in $O(1)$ constant time per protocol cycle.
* Space Constraints: Keeps tracking footprint limits at $O(1)$ constant allocation space.