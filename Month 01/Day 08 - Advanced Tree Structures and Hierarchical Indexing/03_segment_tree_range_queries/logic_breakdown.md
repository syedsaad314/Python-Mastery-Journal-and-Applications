# Logic Breakdown: Segment Tree Interval Metrics
**Engineer:** Syed Saad Bin Irfan

## The Problem
When monitoring telemetry data streams, you frequently need to calculate aggregate metrics (like range sums or minimums) over specific windows. If you use standard loop-based array scans, calculating these aggregates takes linear time. While prefix-sum arrays can speed this up, they fall flat if the underlying data updates frequently, as updating a value forces you to rebuild the array in slow linear time.

## My Approach
I implemented a **Segment Tree** wrapped over a flat array layout. The tree divides the data into a hierarchical map of intervals, where parent nodes pre-calculate and store the aggregate sums of their child nodes. When a query comes in, the engine collects pre-computed values from these interval nodes, avoiding the need to process individual elements one by one.

## Critical Thinking
*   **Time Complexity:** Tree initialization takes $O(N)$ time, while range queries and leaf updates execute reliably in $O(\log N)$ time.
*   **Space Complexity:** Requires a fixed memory allocation bounded at $O(N)$ to hold the underlying segment nodes.

This design is a natural fit for stream analytics engines and high-frequency trading ledgers, where you need to fetch interval summaries over changing data paths without latency spikes.