# Logic Breakdown: Database LRU Page Cache Buffers
**Engineer:** Syed Saad Bin Irfan

## The Problem
Reading structural pages from disk files repeatedly introduces network and drive bottlenecks. We need a fast in-memory look-aside cache to retain high-frequency data blocks while automatically discarding cold data when meeting allocation limits.

## My Approach
I engineered a high-performance **Least Recently Used (LRU) Page Cache** using a hash map combined with a custom doubly linked list structure.

The hash map provides immediate $O(1)$ node selection lookups, while the doubly linked list coordinates usage timelines dynamically. When an element is queried or added, it moves directly to the head position behind the boundary sentinel node. If the cache size exceeds its storage limit, the engine drops the oldest node immediately from the tail position, keeping memory usage constant and protecting the application from resource strain.

## Complexity Profile
* **Runtime Bounds:** Cache queries and placement updates execute in constant $O(1)$ operations.
* **Space Constraints:** Strictly bounded to the explicit capacity slot sizes configured at initialization.