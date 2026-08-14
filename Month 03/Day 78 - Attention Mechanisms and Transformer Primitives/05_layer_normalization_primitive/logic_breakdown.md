# Logic Breakdown: Layer Normalization Primitive
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Batch Normalization computes statistics across the batch index. In NLP sequence modeling, sentences have vastly different lengths, and batch sizes fluctuate. BatchNorm fails completely here because padding tokens heavily skew the batch variance, crashing network stability.

## My Approach
I implemented **Layer Normalization**, calculating $\mu$ and $\sigma^2$ strictly across the `embed_dim` (axis=-1) for *each specific token independently*. The token standardizes its own feature magnitudes before shifting via $\gamma$ and $\beta$. This entirely decouples sequence length and batch sizing from numerical stabilization, stabilizing the deep gradient flows inside Transformer blocks.

## Complexity Profile
* Runtime Bounds: $O(B \cdot N \cdot D)$ executing in parallel across the specific embedding axes.
* Space Constraints: $O(B \cdot N \cdot D)$ temporary footprint allocated for the normalized output matrices.