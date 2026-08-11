# Logic Breakdown: Sigmoid & Tanh Activations
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
For probabilistic binary classification or scenarios requiring bounded outputs, ReLU is insufficient because it grows to infinity. We need mathematical functions that squash outputs into distinct probabilistic bounds without breaking differentiability.

## My Approach
I utilized `np.exp` and `np.tanh` to build vectorized squashing functions. 
1. **Sigmoid** maps $[-\infty, \infty] \rightarrow [0, 1]$, ideal for binary output layers.
2. **Tanh** maps $[-\infty, \infty] \rightarrow [-1, 1]$. Because it is zero-centered, it generally performs better than Sigmoid in hidden layers by feeding centered, normalized data to subsequent layers. 

I explicitly cache the forward activation ($A$) instead of $Z$, because their analytical derivatives ($\sigma \cdot (1-\sigma)$ and $1 - \tanh^2$) can be calculated instantly from $A$, saving expensive re-computations of exponents during backpropagation.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution over matrix structures.
* Space Constraints: $O(N)$ temporary memory to track gradients and cached activation arrays.