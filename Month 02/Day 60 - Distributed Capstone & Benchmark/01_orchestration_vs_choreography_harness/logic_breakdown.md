# Logic Breakdown: Orchestration vs Choreography Harness
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Choosing between a centralized Orchestrator and decentralized Choreography without empirical performance data leads to structural bottlenecks. Orchestration introduces sequential blocking calls, while Choreography risks concurrent execution spikes that are harder to trace.

## My Approach
I built a clean latency benchmark harness using `asyncio.perf_counter`. The test isolates the sequential blocking network path typical of orchestration code and pits it against the concurrent, non-blocking fan-out style used in choreographed event loops.

## Complexity Profile
* Runtime Bounds: Sequential flows run in linear time proportional to cumulative step delays. Parallel execution timelines are bounded by the maximum individual step duration.
* Space Constraints: Maintains an ultra-lightweight, constant memory scale of O(1).