# Logic Breakdown: Vectorized Probability Distributions
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Calculating probabilities for massive datasets iteratively using `math.exp()` over a Python loop causes severe bottlenecks, limiting the capacity to process millions of Bayesian updates or likelihood estimations in real-time.

## My Approach
I expressed the Gaussian probability density function (PDF) entirely in vectorized NumPy calls (`np.exp`, `np.square`, `np.sqrt`). By broadcasting the scalar mean (`mu`) and standard deviation (`sigma`) against the input array `x`, the arithmetic maps cleanly into C-level CPU cache lines and executes simultaneously.

## Complexity Profile
* Runtime Bounds: $O(N)$ executing at optimal C loop speeds for $N$ sample points.
* Space Constraints: $O(N)$ memory required for the intermediate and returned exponent term arrays.