# Logic Breakdown: Causal Look-Ahead Masking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Because Self-Attention evaluates the entire sequence matrix simultaneously, an autoregressive decoder (like GPT) would mathematically "cheat" during training by looking at the subsequent words it is supposed to predict, destroying its predictive capacity.

## My Approach
I generated a static Causal Mask using `np.tril` (Lower Triangle). By mapping future sequence indices to $-1 \times 10^9$ and adding this mask to the raw $QK^T$ scores *before* the Softmax, future tokens mathematically evaluate to $e^{-1e9} \approx 0.0$ in the probability distribution. This explicitly forces token $N$ to route attention strictly to tokens $\le N$.

## Complexity Profile
* Runtime Bounds: $O(N^2)$ execution to generate and add the mask across the attention grid.
* Space Constraints: $O(N^2)$ auxiliary allocation to hold the dense triangular mask matrix.