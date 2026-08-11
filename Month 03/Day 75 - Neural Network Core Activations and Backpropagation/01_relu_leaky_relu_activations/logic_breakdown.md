# Logic Breakdown: ReLU & Leaky ReLU Primitives
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Deep neural networks require non-linear activation functions to learn complex functional mappings. Traditional activations like Sigmoid suffer from vanishing gradients deep in the network, stalling the learning process entirely.

## My Approach
I utilized `np.maximum` and `np.where` to construct vectorized Rectified Linear Units (ReLU). ReLU preserves positive gradients perfectly (derivative of 1), entirely mitigating the vanishing gradient problem for positive outputs. The Leaky ReLU variation assigns a small, non-zero gradient (`alpha`) to negative values, preventing "dying ReLUs" where neurons permanently lock at 0 and cease updating.

## Complexity Profile
* Runtime Bounds: $O(N)$ executing at optimal native array speed over $N$ matrix elements.
* Space Constraints: $O(N)$ for caching the raw $Z$ matrix required to compute the exact derivative during backpropagation.