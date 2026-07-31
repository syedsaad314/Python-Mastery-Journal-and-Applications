# Logic Breakdown: PyArrow Custom Memory Pools & Alignment
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard heap allocators (`malloc`) do not guarantee 64-byte memory boundary alignments. Unaligned data buffers force CPU vector units (AVX-512) to execute extra memory padding passes during SIMD computations.

## My Approach
I used `pa.logging_memory_pool()` and `pa.allocate_buffer()`. PyArrow's C++ underlying memory pool guarantees strict 64-byte memory address alignment, matching CPU cache line boundaries for optimal SIMD execution without unaligned memory access penalties.

## Complexity Profile
* Runtime Bounds: $O(1)$ direct buffer allocation pass.
* Space Constraints: $O(B)$ memory pool allocation where $B$ is requested byte size (1024 bytes).