# Logic Breakdown: Event-Time Watermarking in Structured Streaming
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Stateful stream aggregations (e.g., sliding window sums) retain state in memory indefinitely to handle out-of-order or late-arriving events, causing state stores (RocksDB/In-Memory) to crash due to unbound OOM growth.

## My Approach
I applied `.withWatermark("event_time", "10 minutes")`. PySpark tracks the maximum event time seen by the engine minus the delay threshold (10 minutes). Events older than the trailing watermark boundary are dropped, allowing Spark to clear expired state frames from memory.

## Complexity Profile
* Runtime Bounds: $O(N)$ streaming ingestion and window bucket evaluation pass.
* Space Constraints: $O(W)$ state store memory footprint bounded strictly by watermark window $W$.