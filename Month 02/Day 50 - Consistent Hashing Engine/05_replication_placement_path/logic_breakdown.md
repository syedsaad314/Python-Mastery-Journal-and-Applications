# Logic Breakdown: Replication Placement Paths
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
To survive node failures, data must be duplicated across multiple physical servers. However, since VNodes are interleaved, simply picking the next consecutive slots on the ring could place replicas on the same physical machine.

## My Approach
I built a clockwise traversal engine that tracks physical host identity using a uniqueness set. This ensures replicas are distributed across distinct physical nodes rather than duplicate VNodes on the same machine.

## Complexity Profile
* Runtime Bounds: Traversal takes linear time $O(V)$ in the worst-case scenario.
* Space Constraints: Set lookups track historical hits scaling at $O(N)$ physical limits.