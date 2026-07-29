# Logic Breakdown: Out-Of-Core Streaming Processing
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Datasets larger than RAM crash standard data frame engines during aggregation operations due to full-array allocation spikes.

## My Approach
I used `pl.scan_csv()` combined with `.collect(streaming=True)`. This triggers Polars' streaming engine, which reads and processes data in fixed chunks (mmap / batch iterations), spilling results to sink or reducing aggregations in-flight without holding all raw records simultaneously in memory.

## Complexity Profile
* Runtime Bounds: $O(N)$ linear dataset pass over chunk batches.
* Space Constraints: Strict $O(B)$ memory bound where $B$ is the streaming buffer size.