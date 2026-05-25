# Logic Breakdown: Segment Tree with Lazy Propagation
**Engineer:** Syed Saad Bin Irfan

## The Problem
Modifying individual elements works well for point updates, but updating an entire range element-by-element triggers sequential $O(\log N)$ updates. For large blocks of data, this drops performance down to an inefficient $O(N \log N)$ runtime.

## My Approach
I implemented a **Lazy Segment Tree**. Instead of modifying every affected leaf node immediately during a range update, the engine updates high-level parent segments that match the target range and caches the change for downstream nodes using a matching `lazy` array.

[Node: Range 0-4]  <-- Update applied & cached here
         /         \
[Range 0-2]       [Range 3-4]  <-- Updates pushed down only when queried

These cached updates are only pushed down to child nodes when a query or another update actively accesses that specific path. This lazy optimization ensures that bulk range modifications scale efficiently, matching the performance of single-point updates.

## Complexity Analysis
* **Bulk Range Modifications:** Optimized down to $O(\log N)$.
* **Range Sum Interrogations:** Maintained at a stable $O(\log N)$.
* **Memory Allocations:** Bounded at $O(N)$ using parallel tree arrays.

This structure is a common choice for graphic rendering engines, asset ledger adjustments, and bulk database entry updates.