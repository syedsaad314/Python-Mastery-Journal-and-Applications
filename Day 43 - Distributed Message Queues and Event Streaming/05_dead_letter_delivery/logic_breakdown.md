# Logic Breakdown: Poison Pill Sinks (DLQ)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a consumer encounters a corrupted, unparseable event (a "poison pill"), it will fail repeatedly. If it keeps retrying, it stalls the consumer offset and blocks all subsequent valid messages behind it in the partition.

## My Approach
I implemented a **Dead Letter Queue (DLQ) Streaming Sink Pattern**.

When a message triggers a critical processing exception, the consumer catches the failure, extracts the raw corrupted payload, and forwards it to an isolated, dedicated DLQ stream. The consumer then safely commits its offset and moves on to the next message, preventing a single bad packet from freezing the entire data pipeline.

## Complexity Profile
* **Runtime Bounds:** Error capturing and routing to the DLQ array runs in $O(1)$ constant time.
* **Space Constraints:** Memory usage scales linearly at $O(D)$ relative to total caught failures $D$.