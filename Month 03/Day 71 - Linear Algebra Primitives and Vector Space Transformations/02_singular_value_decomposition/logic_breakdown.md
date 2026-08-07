# Logic Breakdown: Singular Value Decomposition (SVD)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
High-dimensional datasets contain collinear and redundant features. We need a mathematically stable way to extract the axes of maximum variance without losing core informational structure.

## My Approach
I executed SVD via `np.linalg.svd()`. SVD factorizes matrix $A$ into $U \Sigma V^T$. The singular values ($\Sigma$) represent the magnitude of variance along principal axes. By analyzing these values, machine learning models can drop dimensions with near-zero singular values, compressing data with minimal information loss.

## Complexity Profile
* Runtime Bounds: $O(\min(m^2n, mn^2))$ for an $m \times n$ matrix, heavily reliant on LAPACK backend efficiency.
* Space Constraints: $O(m \cdot n)$ to allocate the orthogonal matrices $U$ and $V^T$.