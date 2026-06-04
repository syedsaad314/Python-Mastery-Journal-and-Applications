# Logic Breakdown: Zero-Copy Shared Memory Allocations
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard process communication routes (like Queues or Pipes) rely heavily on Python's `pickle` serialization layer. Passing large datasets across processes forces the OS to serialize data to bytes on one side, transmit it, and reconstruct it into Python objects on the other, creating severe performance hits.

## My Approach
I bypassed the serialization pipeline by utilizing `multiprocessing.shared_memory.SharedMemory` to request a raw byte slice directly from the operating system virtual memory map.

To structure this memory safely without high-level object wrapping, I used the native `struct` library to layout a fixed-size binary schema (`qqd` representing two 64-bit integers and one double-precision float). Because both child and parent processes point to the same physical RAM addresses, updates occur instantly and with zero copy operations.

## Complexity Profile
* **Runtime Bounds:** Constant $O(1)$ read and write performance bounds.
* **Space Constraints:** Strictly bounded to $24$ bytes of persistent physical memory allocations.