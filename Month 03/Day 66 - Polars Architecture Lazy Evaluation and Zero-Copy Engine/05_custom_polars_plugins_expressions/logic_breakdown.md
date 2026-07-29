# Logic Breakdown: Groupwise Window Expressions (`.over()`)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard SQL or Pandas group-by aggregations collapse row dimensions. Calculating row-level relative metrics against group statistics requires extra joins or `transform()` passes.

## My Approach
I implemented Polars `.over()` window expressions. Polars calculates group metrics in parallel and broadcasts results back to match original row indices, retaining initial schema dimensions in a single efficient execution pass.

## Complexity Profile
* Runtime Bounds: $O(N \log N)$ due to internal group index sorting pass.
* Space Constraints: $O(N)$ space required to track group offset mappings.