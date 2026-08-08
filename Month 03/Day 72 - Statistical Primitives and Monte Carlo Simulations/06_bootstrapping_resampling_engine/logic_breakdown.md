# Logic Breakdown: Empirical Bootstrapping Engine
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Parametric statistics require strict assumptions (e.g., normal distribution). When data is highly skewed or non-parametric, standard confidence intervals break down completely. Looping iteratively to redraw thousands of sub-samples manually freezes Python processes.

## My Approach
I implemented fully vectorized bootstrapping. `rng.integers()` generates an $I \times N$ matrix of indices representing all iterations and draws in a single C-level operation. Advanced array indexing (`data[random_indices]`) pulls the raw values, and `np.mean(axis=1)` collapses the matrix into an empirical distribution map of size $I$ instantly.

## Complexity Profile
* Runtime Bounds: $O(I \cdot N)$ executing at maximum C-level RAM indexing velocity.
* Space Constraints: $O(I \cdot N)$ memory capacity to hold the comprehensive bootstrapped sub-samples matrix.