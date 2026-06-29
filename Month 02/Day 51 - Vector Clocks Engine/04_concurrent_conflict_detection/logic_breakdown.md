# Logic Breakdown: Concurrent Conflict Detection
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When a network split happens, nodes on both sides of the partition might accept updates simultaneously. The system needs to flag these parallel updates as concurrent conflicts so it can preserve both versions instead of silently dropping data.

## My Approach
I built an algebraic divergence analyzer. If Vector A contains a counter value that is larger than Vector B's corresponding entry, while Vector B also contains an entry larger than Vector A's, the updates are flagged as concurrent conflicts.

## Complexity Profile
* Runtime Bounds: Operates in linear time $O(N)$ over the combined key maps.
* Space Constraints: Uses memory space of $O(N)$ to build comparison sets.