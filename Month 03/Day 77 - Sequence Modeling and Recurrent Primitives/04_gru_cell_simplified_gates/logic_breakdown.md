# Logic Breakdown: GRU Cell Simplified Gates
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
LSTMs are powerful but computationally expensive, requiring 4 massive separate matrix multiplications (or one 4x sized one) per step and dual state tracking ($C$ and $H$).

## My Approach
I implemented the Gated Recurrent Unit (GRU). The GRU drops the Cell state entirely and couples the `Forget` and `Input` mechanics into a single `Update Gate` ($z_t$). The algorithm calculates a linear interpolation between the historical state and the new candidate state: $h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$. This requires only 3 matrix multiplications instead of 4, dropping memory usage and FLOPs by 25% while maintaining similar gradient stabilization.

## Complexity Profile
* Runtime Bounds: $O((H + X) \cdot 3H)$ lowering the constant factor overhead relative to LSTMs.
* Space Constraints: $O(H)$ state bound, eliminating the secondary auxiliary memory vector.