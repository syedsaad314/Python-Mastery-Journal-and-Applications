# Logic Breakdown: Compute Loop Itertools Optimization
**Engineer:** Syed Saad Bin Irfan

## The Problem
Relying on explicit `.append()` calls inside standard Python `for` loops introduces substantial interpreter instruction overhead, slowing down time-sensitive compute cycles.

## My Approach
I benchmarked explicit manual loops against highly optimized internal list comprehensions that leverage C-level optimizations inside the CPython virtual machine.

By avoiding individual `.append` global attribute lookups on every loop iteration, the optimized pipeline runs entirely within compiled C-level loops. This minimizes runtime instruction steps, providing clean, native acceleration without requiring external math packages.

## Complexity Profile
* **Runtime Bounds:** Processes linearly at $O(N)$ speed, but minimizes instruction overhead.
* **Space Constraints:** Scales at $O(N)$ space requirements to store the transformed array.