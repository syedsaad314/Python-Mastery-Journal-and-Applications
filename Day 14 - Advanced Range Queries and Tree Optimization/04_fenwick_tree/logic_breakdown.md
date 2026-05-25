# Logic Breakdown: Fenwick Tree (Binary Indexed Tree)
**Engineer:** Syed Saad Bin Irfan

## The Problem
While Segment Trees are highly flexible, they require extra memory blocks up to four times the size of the source array ($4N$). In memory-constrained systems like network routers or high-frequency frequency counters, we need a lighter approach that still offers logarithmic performance.

## My Approach
I implemented a **Fenwick Tree** (also known as a **Binary Indexed Tree**). This structure stores precalculated cumulative intervals using a single array of size $N+1$, aligning tree offsets with the binary representations of their indices.

The key optimization relies on two bitwise properties:
1. **Stepping Forward (`i += (i & -i)`):** Isolates the lowest set bit of an index and adds it. This moves the pointer forward to update all higher-level parent intervals that contain the current node.
2. **Stepping Backward (`i -= (i & -i)`):** Subtracts the lowest set bit, allowing the pointer to jump backward and quickly collect precalculated prefix segments.

Interval queries are resolved by calculating the difference between two prefix sums:

$$\text{RangeSum}(L, R) = \text{PrefixSum}(R) - \text{PrefixSum}(L-1)$$

## Complexity Evaluation
* **Point Adjustments:** Bounded at $O(\log N)$ bitwise transformations.
* **Prefix Interrogations:** Completed in $O(\log N)$ steps.
* **Space Efficiency:** $O(N)$ space using a single flat array layout.

This lightweight footprint makes it a standard choice for tracking running frequencies, cumulative data streams, and database index offsets.