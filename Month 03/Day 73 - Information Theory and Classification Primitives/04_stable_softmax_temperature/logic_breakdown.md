# Logic Breakdown: Numerically Stable Softmax & Temperature
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Exponentiating raw neural network logits (`np.exp(1000)`) triggers immediate numerical overflow (`NaN` or `Inf`), breaking model tracking gradients entirely.

## My Approach
I subtracted the maximum logit value from the entire array prior to exponentiation ($x_i - \max(x)$). Because $\frac{e^{x - c}}{\sum e^{x - c}} = \frac{e^x}{\sum e^x}$, this mathematical trick preserves the exact probability distribution while capping the maximum exponent at `0` (which safely evaluates to `1.0`). I also implemented Temperature Scaling ($T$), where $T > 1$ softens confidence, allowing generative models to produce more diverse outputs.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution speed over the logit array.
* Space Constraints: $O(N)$ to allocate the exponentiated matrix fields.