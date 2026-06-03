# Logic Breakdown: Programmatic CPU Profiling
**Engineer:** Syed Saad Bin Irfan

## The Problem
Guessing which functions cause latency issues across large applications leads to wasted optimization efforts and unoptimized code segments.

## My Approach
I integrated a programmatic tracing layer using the native `cProfile` and `pstats` modules. 

Instead of wrapping code blocks with basic `time.perf_counter()` metrics, this approach monitors call sequences across the target workload. By sorting the output report by `pstats.SortKey.TIME`, the developer can pinpoint exactly which subfunctions consume the most internal processing time, isolating hotspots without changing the overall application code.

## Complexity Profile
* **Runtime Bounds:** Adding a profiler introduces a small, uniform timing overhead ($O(1)$) per monitored call stack layer.
* **Space Constraints:** Minimal memory footprint needed to capture stack trace statistics.