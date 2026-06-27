# Logic Breakdown: Bounded Load Consistent Hashing
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Even with VNodes, highly popular keys (e.g., viral data) can overwhelm a single node, leading to severe resource imbalances.

## My Approach
I implemented a capacity tracking layer. If a node's load exceeds the configured safety threshold, the router dynamically forwards the key to the next available node down the ring.

## Complexity Profile
* Runtime Bounds: $O(F)$ matching the length of the fallback node array.
* Space Constraints: Scaled at $O(N)$ memory tracks relative to physical hosts.