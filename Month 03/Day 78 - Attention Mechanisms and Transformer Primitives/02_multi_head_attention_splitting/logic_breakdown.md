# Logic Breakdown: Multi-Head Attention Splitting
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
A single attention operation forces the network to average out its focus, meaning it struggles to simultaneously track different structural nuances (e.g., subject-verb relationships vs. adjective-noun modifiers) in the same sentence.

## My Approach
I implemented the Tensor Splitting primitive for Multi-Head Attention. By taking the full embedding dimension (e.g., 512) and reshaping it into separate sub-matrices (e.g., 8 heads of 64 dimensions each), the model creates parallel representation subspaces. The `transpose(0, 2, 1, 3)` call strategically shifts the `num_heads` axis forward, allowing underlying C/BLAS libraries to execute batched matrix multiplications for all heads simultaneously without interference.

## Complexity Profile
* Runtime Bounds: $O(1)$ constant time execution via NumPy strided memory manipulation.
* Space Constraints: $O(N \cdot D)$ temporary allocation overhead when transposing creates non-contiguous array copies.