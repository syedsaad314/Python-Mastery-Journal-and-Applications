# Logic Breakdown: Partial Order Comparison Operations
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
To safely accept updates without a central coordinator, a node must determine if an incoming write is a direct descendant of its local data or an outdated, duplicate message.

## My Approach
I implemented a partial order evaluation function based on vector clock rules: Vector A causally precedes Vector B if every entry in A is less than or equal to its corresponding entry in B, and at least one entry is strictly smaller.

## Complexity Profile
* Runtime Bounds: Scans in linear time $O(N)$ relative to the total number of unique keys inside the vectors.
* Space Constraints: Allocates memory linearly at $O(N)$ to unify key fields during comparison checks.