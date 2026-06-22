# Logic Breakdown: Standard Segment Tree (Point Updates)
**Engineer:** Syed Saad Bin Irfan

## The Problem
If data updates frequently, static structures like Sparse Tables fall short because any change forces an expensive recalculation. We need a structure that balances both operations—allowing us to update individual elements and query full ranges without performance taking a hit.

## My Approach
I implemented a standard **Segment Tree**. This structure splits the array into a binary tree layout where each leaf represents a single array element, and each internal parent node holds the aggregated sum of its underlying range segments.

1. **Querying:** When searching a range $[L, R]$, the tree splits the request. Ranges that fall entirely inside the query return their precalculated sums immediately, while partially overlapping paths branch downward. Completely unrelated nodes are bypassed entirely.
2. **Updating:** When a single element changes, the engine navigates straight down to that specific leaf node in $O(\log N)$ time. As the recursive functions return, parent nodes recalculate their values to keep the tree accurate.

## Complexity Profile
* **Tree Generation:** $O(N)$ allocation steps.
* **Point Modification:** $O(\log N)$ structural traversals.
* **Range Interrogation:** $O(\log N)$ execution steps.
* **Space Overhead:** $O(N)$ space (using a flat array of size $4N$ to map nodes safely).

This provides a highly flexible foundation for dynamic systems that need to maintain running metrics over fluid datasets.