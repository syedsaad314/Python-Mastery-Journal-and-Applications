# Logic Breakdown: Vectorized Batch UDF Execution
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Using `map_elements()` forces Polars to deserialize every single value to a Python object, run Python scalar byte code, and serialize back, causing massive GIL performance slowdowns.

## My Approach
I implemented `.map_batches()`. Instead of looping row-by-row, Polars passes the underlying Arrow Series array directly to the transformation function, executing in a single vectorized call and preserving Arrow zero-copy memory buffers.

## Complexity Profile
* Runtime Bounds: $O(1)$ Python function invocation overhead; $O(N)$ native C/Rust vectorized execution.
* Space Constraints: $O(N)$ contiguous series vector result buffer allocation.