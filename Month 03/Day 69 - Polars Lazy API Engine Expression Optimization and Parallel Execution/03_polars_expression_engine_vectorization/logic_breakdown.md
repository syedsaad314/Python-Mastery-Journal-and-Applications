# Logic Breakdown: Polars Expression Engine Vectorization
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Using Python `if/else` logic inside custom row-level functions (`apply()` or `lambda`) drops out of vectorized execution, triggering slow Python interpreter loops and GIL blocking.

## My Approach
I composed a context expression using `pl.when().then().otherwise()`. Polars transforms expression trees into low-level SIMD operations written in Rust, running directly over contiguous Arrow memory arrays without stepping back into Python runtime context.

## Complexity Profile
* Runtime Bounds: $O(N)$ linear time SIMD execution pass.
* Space Constraints: $O(N)$ contiguous output buffer allocation.