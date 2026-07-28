# Logic Breakdown: Zero-Stride Matrix Broadcasting
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When performing element-wise arithmetic between arrays of unequal shapes (e.g., adding a 1D bias vector to a 2D feature matrix), duplicating the smaller array to match dimensions wastes significant memory bandwidth.

## My Approach
NumPy resolves shape mismatches through virtual broadcasting. When expanding a singleton dimension, NumPy assigns a stride of `0` bytes along that axis. When the C execution loop advances along the broadcasted axis, pointer arithmetic steps by `0` bytes, repeatedly reading the same memory location at hardware speed without duplicating memory.

## Complexity Profile
* Runtime Bounds: True deterministic O(1) broadcasting view setup.
* Space Constraints: O(1) constant overhead; zero new matrix allocations.