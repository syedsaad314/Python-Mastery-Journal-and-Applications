# Logic Breakdown: Event Tracing Telemetry
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Debugging a choreographed architecture can feel impossible because execution paths are scattered across dozens of unlinked event streams. If an order gets stuck, finding out where the pipeline stalled without a unified trace log requires digging through multiple disconnected logs.

## My Approach
I built a centralized tracking pipeline simulator that logs lifecycle updates using an immutable tracking token (`correlation_id`). This lets you query the system history to rebuild the exact execution path across all decoupled layers.

## Complexity Profile
* Runtime Bounds: Appending log events is O(1). Reconstructing the full pipeline path runs in linear O(T) time across total trace records.
* Space Constraints: Footprint scales linearly at O(T) to store the telemetry logs.