# Logic Breakdown: Inverted Dropout Regularization
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Dense layers often over-rely on a few dominating feature nodes, leading to severe model overfitting (co-adaptation). Standard dropout forces scaling adjustments during inference (production phase), complicating deployment code.

## My Approach
I constructed the **Inverted Dropout** matrix implementation. By generating a boolean matrix `D_mask` from a uniform distribution ($< \text{keep\_prob}$), we zero out random nodes instantly. 
Crucially, I divide the remaining active nodes by `keep_prob` during the *forward training pass*. This ensures the mathematical expected value of the layer's output remains completely identical. In production (inference), we simply turn dropout off and do nothing, bypassing production scaling bugs entirely.

## Complexity Profile
* Runtime Bounds: $O(N)$ generating random masking vectors across the layer arrays.
* Space Constraints: $O(N)$ memory cost for maintaining the stochastic boolean cache mask.