# Logic Breakdown: He & Xavier Weight Initialization
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Initializing network weights to static zeros breaks symmetry, causing all neurons to compute identical gradients. Initializing them to random standard normals causes variance to multiply exponentially across layers, either blowing up the gradients (`Inf`) or shrinking them to zero (Vanishing Gradients).

## My Approach
I utilized statistically precise matrix initialization functions.
1. **Xavier (Glorot):** Samples weights from a distribution parameterized by $\sqrt{\frac{2}{n_{in} + n_{out}}}$. It keeps signal variance identical across layers using Sigmoid/Tanh functions.
2. **He (Kaiming):** Parameterized by $\sqrt{\frac{2}{n_{in}}}$. It explicitly accounts for the mathematical reality that ReLU activations zero out exactly half the data space, doubling the variance preservation to compensate.

## Complexity Profile
* Runtime Bounds: $O(M \cdot N)$ dictated by the NumPy random generation stream mapping.
* Space Constraints: $O(M \cdot N)$ allocation for the respective neural layer connection matrix.