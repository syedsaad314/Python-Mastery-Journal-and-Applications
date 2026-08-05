# Logic Breakdown: PyArrow Vectorized PySpark UDFs
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard PySpark Python UDFs serialize Java objects to Python objects row-by-row over socket IPC connections, incurring extreme serialization latency and disabling SIMD vector optimizations.

## My Approach
I implemented PyArrow-accelerated Pandas UDFs (`@pandas_udf`). PySpark converts JVM memory blocks directly to Apache Arrow IPC record batches zero-copy, streaming data batches into Python worker processes for high-speed SIMD vector calculations.

## Complexity Profile
* Runtime Bounds: $O(N / B)$ batch IPC transfers where $N$ is total rows and $B$ is Arrow batch size.
* Space Constraints: $O(B)$ memory buffer allocation for stream record batches.