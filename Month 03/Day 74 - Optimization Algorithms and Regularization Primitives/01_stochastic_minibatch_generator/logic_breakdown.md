# Logic Breakdown: Stochastic Mini-Batch Generation
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Full-batch Gradient Descent requires calculating gradients over the entire dataset before making a single parameter update. This is computationally agonizing on millions of rows and physically exceeds GPU VRAM limits. Pure Stochastic Gradient Descent (batch size = 1) is too noisy and fails to utilize matrix multiplication (BLAS) vectorization.

## My Approach
I built a Python `Generator` that shuffles index pointers and yields chunked memory views of the array (`X[batch_indices]`). This "Mini-Batch" approach strikes the optimal mathematical balance: providing enough data for high-speed SIMD matrix multiplication while updating model weights frequently enough to navigate complex loss topologies rapidly.

## Complexity Profile
* Runtime Bounds: $O(N)$ shuffling pass, followed by $O(B)$ memory lookups per batch.
* Space Constraints: $O(N)$ to store the randomized index permutation array.