# Logic Breakdown: Batch Normalization Matrix Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
As parameters update, the distribution of intermediate activations shifts drastically (Internal Covariate Shift), forcing subsequent layers to continuously re-adapt to new incoming numerical scales, destabilizing training.

## My Approach
I isolated the exact Batch Normalization primitive mapping. 
First, the engine normalizes the current batch ($Z$) to a zero-mean and unit-variance state: $Z_{norm} = \frac{Z - \mu}{\sqrt{\sigma^2 + \epsilon}}$. 
Second, it allows the network to recover expressiveness by learning optimal scale ($\gamma$) and shift ($\beta$) vectors: $\tilde{Z} = \gamma Z_{norm} + \beta$. 
Crucially, it computes an Exponentially Weighted Moving Average (EWMA) of $\mu$ and $\sigma^2$ during the `train` mode, which acts as the frozen baseline population statistic later during the `test` phase.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution operating flawlessly across SIMD memory chunks.
* Space Constraints: $O(N)$ for the resultant normalized output matrices and $O(F)$ bounded footprint for the continuous EWMA moving statistic trackers.