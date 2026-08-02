# Logic Breakdown: Tungsten Off-Heap Memory Management
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard JVM Java object representations carry heavy object header overhead (16+ bytes per object) and trigger severe Garbage Collection (GC) execution pauses when processing multi-gigabyte heap spaces.

## My Approach
I configured Project Tungsten via `spark.memory.offHeap.enabled=true`. Tungsten replaces Java heap objects with contiguous `UnsafeRow` memory encodings managed off-heap via direct C-style pointer offsets (`sun.misc.Unsafe`), bypassing JVM GC overhead and maximizing CPU L1/L2 cache locality.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution pass with near-zero GC pause overhead.
* Space Constraints: Strict $O(M)$ off-heap memory allocation bound where $M = 64\text{MB}$.