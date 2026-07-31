# Logic Breakdown: SIMD-Accelerated PyArrow Compute Kernels
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Filtering and aggregating data using native Python functions (`sum()`, list comprehensions) re-introduces GIL interpreter overhead and invalidates CPU SIMD instruction vectorization.

## My Approach
I used `pyarrow.compute` kernels (`pc.greater()`, `pc.filter()`, `pc.sum()`). PyArrow routes these calls directly to C++ Acero/Arrow execution modules, leveraging CPU SIMD registers to evaluate vector blocks concurrently.

## Complexity Profile
* Runtime Bounds: $O(N)$ linear vectorized pass over array memory.
* Space Constraints: $O(K)$ temporary vector allocation for boolean mask where $K = N$.